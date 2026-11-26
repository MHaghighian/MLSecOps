# Kubernetes AI/LLM inference workload admission policy (Ch.3, Ch.5, Ch.16, Appendix E.7.3).
# Uses package mlsecops.k8s so it stays isolated from top-level Evidence Pack (`package main`) checks.
# Run: conftest test --policy policies/k8s --namespace mlsecops.k8s <manifest.yaml>
package mlsecops.k8s

import rego.v1

workload_kinds := {"Pod", "Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob"}

sensitive_env_name(name) if {
	upper(name) in {"HF_TOKEN", "VLLM_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "AWS_SECRET_ACCESS_KEY"}
} else if {
	regex.match("(?i)(^|_)(TOKEN|SECRET|API_KEY|PASSWORD)$", name)
}

pod_spec := input.spec if {
	input.kind == "Pod"
} else := input.spec.template.spec if {
	input.kind in {"Deployment", "StatefulSet", "DaemonSet", "Job"}
} else := input.spec.jobTemplate.spec.template.spec if {
	input.kind == "CronJob"
}

all_containers contains c if {
	some c in object.get(pod_spec, "containers", [])
}

all_containers contains c if {
	some c in object.get(pod_spec, "initContainers", [])
}

is_digest_pinned(image) if {
	is_string(image)
	regex.match("@sha256:[a-f0-9]{64}$", image)
}

has_run_as_non_root if {
	pod_spec.securityContext.runAsNonRoot == true
	not any_container_runs_as_root
} else if {
	count(all_containers) > 0
	every c in all_containers {
		c.securityContext.runAsNonRoot == true
		object.get(c.securityContext, "runAsUser", object.get(pod_spec.securityContext, "runAsUser", 1000)) != 0
	}
}

any_container_runs_as_root if {
	some c in all_containers
	c.securityContext.runAsNonRoot == false
} else if {
	some c in all_containers
	c.securityContext.runAsUser == 0
} else if {
	pod_spec.securityContext.runAsUser == 0
}

has_seccomp_profile if {
	pod_spec.securityContext.seccompProfile.type in {"RuntimeDefault", "Localhost"}
	not any_container_disables_seccomp
} else if {
	count(all_containers) > 0
	every c in all_containers {
		c.securityContext.seccompProfile.type in {"RuntimeDefault", "Localhost"}
	}
}

any_container_disables_seccomp if {
	some c in all_containers
	c.securityContext.seccompProfile.type == "Unconfined"
}

drops_all_capabilities(c) if {
	some cap in c.securityContext.capabilities.drop
	upper(cap) == "ALL"
}

# Ch.16: every container image must be pinned to an immutable sha256 digest (reject :latest / mutable tags).
deny contains msg if {
	input.kind in workload_kinds
	some c in all_containers
	img := object.get(c, "image", "")
	not is_digest_pinned(img)
	msg := sprintf("CRITICAL [Ch.16/CP9]: container %q image %q must be pinned with @sha256:<64-hex> digest", [c.name, img])
}

# Ch.5/Ch.16: disallow remote-code execution at model load (--trust-remote-code / TRUST_REMOTE_CODE).
deny contains msg if {
	input.kind in workload_kinds
	some c in all_containers
	some token in array.concat(object.get(c, "command", []), object.get(c, "args", []))
	contains(lower(token), "--trust-remote-code")
	msg := sprintf("CRITICAL [Ch.5/16]: container %q passes --trust-remote-code (remote RCE vector)", [c.name])
}

deny contains msg if {
	input.kind in workload_kinds
	some c in all_containers
	some env in object.get(c, "env", [])
	upper(env.name) in {"TRUST_REMOTE_CODE", "HF_HUB_TRUST_REMOTE_CODE"}
	lower(object.get(env, "value", "")) in {"1", "true", "yes"}
	msg := sprintf("CRITICAL [Ch.5/16]: container %q enables %s=%v", [c.name, env.name, env.value])
}

# Ch.16: reject plaintext secret literals in container env or CLI command/args tokens.
deny contains msg if {
	input.kind in workload_kinds
	some c in all_containers
	some env in object.get(c, "env", [])
	sensitive_env_name(env.name)
	val := object.get(env, "value", "")
	is_string(val)
	count(trim_space(val)) > 0
	not env.valueFrom
	msg := sprintf("CRITICAL [Ch.5/16]: container %q hardcodes sensitive env %q inline instead of valueFrom", [c.name, env.name])
}

deny contains msg if {
	input.kind in workload_kinds
	some c in all_containers
	some token in array.concat(object.get(c, "command", []), object.get(c, "args", []))
	is_string(token)
	regex.match("(sk-(?:proj-)?[A-Za-z0-9_-]{20,}|hf_[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|glpat-[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|A(?:KIA|SIA)[0-9A-Z]{16})", token)
	msg := sprintf("CRITICAL [Ch.5/16]: container %q exposes hardcoded token literal in command/args", [c.name])
}

deny contains msg if {
	input.kind in workload_kinds
	some c in all_containers
	args := array.concat(object.get(c, "command", []), object.get(c, "args", []))
	some i, token in args
	is_string(token)
	token == "--allowed-local-media-path"
	i + 1 < count(args)
	media_root := trim_space(args[i + 1])
	media_root in {"/", "/etc", "/root", "/var", "/home"}
	msg := sprintf("HIGH [Ch.16]: container %q sets dangerous --allowed-local-media-path=%q (LFI risk)", [c.name, media_root])
}

# Ch.16: reject host namespace breakouts and hostPath mounts.
deny contains msg if {
	input.kind in workload_kinds
	pod_spec.hostNetwork == true
	msg := sprintf("CRITICAL [Ch.16]: %s %q must not enable hostNetwork=true", [input.kind, object.get(input.metadata, "name", "<unnamed>")])
}

deny contains msg if {
	input.kind in workload_kinds
	pod_spec.hostPID == true
	msg := sprintf("CRITICAL [Ch.16]: %s %q must not enable hostPID=true", [input.kind, object.get(input.metadata, "name", "<unnamed>")])
}

deny contains msg if {
	input.kind in workload_kinds
	pod_spec.hostIPC == true
	msg := sprintf("CRITICAL [Ch.16]: %s %q must not enable hostIPC=true", [input.kind, object.get(input.metadata, "name", "<unnamed>")])
}

deny contains msg if {
	input.kind in workload_kinds
	some vol in object.get(pod_spec, "volumes", [])
	vol.hostPath
	msg := sprintf("CRITICAL [Ch.16]: volume %q mounts hostPath (container escape risk)", [vol.name])
}

deny contains msg if {
	input.kind in workload_kinds
	some c in all_containers
	some port in object.get(c, "ports", [])
	port.hostPort
	msg := sprintf("HIGH [Ch.16]: container %q binds hostPort %v (bypasses gateway/NetworkPolicy)", [c.name, port.hostPort])
}

# Ch.16: reject unauthenticated vLLM inference containers and direct LoadBalancer/NodePort/externalIPs exposure.
vllm_auth_configured(c) if {
	some env in object.get(c, "env", [])
	upper(env.name) == "VLLM_API_KEY"
	env.valueFrom
} else if {
	some env in object.get(c, "env", [])
	upper(env.name) == "VLLM_API_KEY"
	is_string(object.get(env, "value", ""))
	count(trim_space(env.value)) > 0
} else if {
	some token in array.concat(object.get(c, "command", []), object.get(c, "args", []))
	is_string(token)
	regex.match("^--api-key(?:=.+)?$", lower(token))
	not lower(token) == "--api-key="
}

deny contains msg if {
	input.kind in workload_kinds
	some c in object.get(pod_spec, "containers", [])
	contains(lower(object.get(c, "image", "")), "vllm")
	not vllm_auth_configured(c)
	msg := sprintf("HIGH [Ch.16]: vLLM container %q must configure VLLM_API_KEY or --api-key auth", [c.name])
}

deny contains msg if {
	input.kind == "Service"
	input.spec.type in {"LoadBalancer", "NodePort"}
	msg := sprintf("HIGH [Ch.16]: Service %q uses %s (do not expose inference pods without gateway/WAF)", [object.get(input.metadata, "name", "<unnamed>"), input.spec.type])
}

deny contains msg if {
	input.kind == "Service"
	count(object.get(input.spec, "externalIPs", [])) > 0
	msg := sprintf("HIGH [Ch.16]: Service %q defines spec.externalIPs (CVE-2020-8554 exposure vector)", [object.get(input.metadata, "name", "<unnamed>")])
}

# Ch.16: Pod Security Standards restricted — non-root, seccomp, privilege boundaries, read-only rootfs, dropped caps.
deny contains msg if {
	input.kind in workload_kinds
	some c in all_containers
	c.securityContext.privileged == true
	msg := sprintf("CRITICAL [Ch.16]: container %q must not run privileged=true", [c.name])
}

deny contains msg if {
	input.kind in workload_kinds
	some c in all_containers
	not c.securityContext.allowPrivilegeEscalation == false
	msg := sprintf("HIGH [Ch.16]: container %q must set securityContext.allowPrivilegeEscalation=false", [c.name])
}

deny contains msg if {
	input.kind in workload_kinds
	not has_run_as_non_root
	msg := sprintf("HIGH [Ch.16]: %s %q must enforce securityContext.runAsNonRoot=true", [input.kind, object.get(input.metadata, "name", "<unnamed>")])
}

deny contains msg if {
	input.kind in workload_kinds
	not has_seccomp_profile
	msg := sprintf("HIGH [Ch.16]: %s %q must enforce seccompProfile RuntimeDefault or Localhost", [input.kind, object.get(input.metadata, "name", "<unnamed>")])
}

deny contains msg if {
	input.kind in workload_kinds
	some c in all_containers
	not drops_all_capabilities(c)
	msg := sprintf("HIGH [Ch.16]: container %q must drop ALL capabilities", [c.name])
}

deny contains msg if {
	input.kind in workload_kinds
	some c in all_containers
	c.securityContext.procMount == "Unmasked"
	msg := sprintf("CRITICAL [Ch.16]: container %q must not set procMount=Unmasked", [c.name])
}

deny contains msg if {
	input.kind in workload_kinds
	some c in all_containers
	some cap in object.get(object.get(object.get(c, "securityContext", {}), "capabilities", {}), "add", [])
	upper(cap) != "NET_BIND_SERVICE"
	msg := sprintf("HIGH [Ch.16]: container %q must not add privileged capability %q", [c.name, cap])
}

deny contains msg if {
	input.kind in workload_kinds
	some c in object.get(pod_spec, "containers", [])
	not c.securityContext.readOnlyRootFilesystem == true
	msg := sprintf("MEDIUM [Ch.16]: container %q should set securityContext.readOnlyRootFilesystem=true", [c.name])
}

# Ch.3/Ch.16: inference pods require bounded resources (compute hijacking protection) and no SA token auto-mount.
deny contains msg if {
	input.kind in workload_kinds
	some c in object.get(pod_spec, "containers", [])
	not c.resources.limits.memory
	msg := sprintf("MEDIUM [Ch.3/16]: container %q must define resources.limits.memory", [c.name])
}

deny contains msg if {
	input.kind in workload_kinds
	not pod_spec.automountServiceAccountToken == false
	msg := sprintf("HIGH [Ch.16]: %s %q must set automountServiceAccountToken=false on inference workloads", [input.kind, object.get(input.metadata, "name", "<unnamed>")])
}
