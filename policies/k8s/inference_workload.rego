# Kubernetes AI/LLM inference workload admission policy (Ch.16 / Appendix E.7.3).
# Uses package mlsecops.k8s so it stays isolated from top-level Evidence Pack (`package main`) checks.
# Run: conftest test --policy policies/k8s --namespace mlsecops.k8s <manifest.yaml>
package mlsecops.k8s

import rego.v1

workload_kinds := {"Pod", "Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob"}

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
} else if {
	count(all_containers) > 0
	every c in all_containers {
		c.securityContext.runAsNonRoot == true
	}
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

# Ch.16: reject privileged containers and missing allowPrivilegeEscalation=false.
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

# Ch.16: Pod Security Standards restricted — non-root execution and dropped Linux capabilities.
deny contains msg if {
	input.kind in workload_kinds
	not has_run_as_non_root
	msg := sprintf("HIGH [Ch.16]: %s %q must enforce securityContext.runAsNonRoot=true", [input.kind, object.get(input.metadata, "name", "<unnamed>")])
}

deny contains msg if {
	input.kind in workload_kinds
	some c in all_containers
	not drops_all_capabilities(c)
	msg := sprintf("HIGH [Ch.16]: container %q must drop ALL capabilities", [c.name])
}

# Ch.16: inference pods should not auto-mount Kubernetes API credentials by default.
deny contains msg if {
	input.kind in workload_kinds
	not pod_spec.automountServiceAccountToken == false
	msg := sprintf("HIGH [Ch.16]: %s %q must set automountServiceAccountToken=false on inference workloads", [input.kind, object.get(input.metadata, "name", "<unnamed>")])
}
