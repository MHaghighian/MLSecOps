package mlsecops.k8s_test

import data.mlsecops.k8s
import rego.v1

pinned_img := "ghcr.io/example/vllm-openai@sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

base_deploy := {
	"apiVersion": "apps/v1",
	"kind": "Deployment",
	"metadata": {"name": "llm-inference", "namespace": "ai-inference"},
	"spec": {
		"template": {
			"spec": {
				"automountServiceAccountToken": false,
				"securityContext": {
					"runAsNonRoot": true,
					"seccompProfile": {"type": "RuntimeDefault"},
				},
				"containers": [{
					"name": "vllm",
					"image": pinned_img,
					"env": [{"name": "VLLM_API_KEY", "valueFrom": {"secretKeyRef": {"name": "inference-api-key", "key": "VLLM_API_KEY"}}}],
					"resources": {"limits": {"cpu": "4", "memory": "16Gi"}},
					"securityContext": {
						"allowPrivilegeEscalation": false,
						"readOnlyRootFilesystem": true,
						"capabilities": {"drop": ["ALL"]},
					},
				}],
			},
		},
	},
}

test_valid_deployment_passes if {
	count(k8s.deny) == 0 with input as base_deploy
}

test_deny_unpinned_and_trust_remote_code_and_plain_secret if {
	bad := object.union(base_deploy, {"spec": {"template": {"spec": {"containers": [{
		"name": "vllm",
		"image": "vllm/vllm-openai:latest",
		"args": ["--model", "org/m", "--trust-remote-code", "--api-key", "hf_abcdefghijklmnopqrstuvwxyz123456"],
		"env": [{"name": "HF_TOKEN", "value": "hf_plaintext_secret"}],
		"resources": {"limits": {"memory": "16Gi"}},
		"securityContext": {
			"allowPrivilegeEscalation": false,
			"readOnlyRootFilesystem": true,
			"capabilities": {"drop": ["ALL"]},
		},
	}]}}}})
	some m1 in k8s.deny with input as bad
	contains(m1, "CRITICAL [Ch.16/CP9]: container")
	some m2 in k8s.deny with input as bad
	contains(m2, "CRITICAL [Ch.5/16]: container \"vllm\" passes --trust-remote-code")
	some m3 in k8s.deny with input as bad
	contains(m3, "CRITICAL [Ch.5/16]: container \"vllm\" hardcodes sensitive env")
	some m4 in k8s.deny with input as bad
	contains(m4, "exposes hardcoded token literal in command/args")
}

test_deny_container_overrides_pod_security if {
	bad := object.union(base_deploy, {"spec": {"template": {"spec": {"containers": [{
		"name": "vllm",
		"image": pinned_img,
		"resources": {"limits": {"memory": "16Gi"}},
		"securityContext": {
			"runAsUser": 0,
			"allowPrivilegeEscalation": false,
			"readOnlyRootFilesystem": true,
			"seccompProfile": {"type": "Unconfined"},
			"capabilities": {"drop": ["ALL"]},
		},
	}]}}}})
	some m_root in k8s.deny with input as bad
	contains(m_root, "runAsNonRoot=true")
	some m_sec in k8s.deny with input as bad
	contains(m_sec, "seccompProfile")
}

test_deny_exposure_and_unauthenticated_vllm if {
	bad_svc := {
		"apiVersion": "v1",
		"kind": "Service",
		"metadata": {"name": "vllm-public"},
		"spec": {"type": "LoadBalancer"},
	}
	some m_svc in k8s.deny with input as bad_svc
	contains(m_svc, "LoadBalancer")

	bad_port := object.union(base_deploy, {"spec": {"template": {"spec": {"containers": [{
		"name": "vllm",
		"image": pinned_img,
		"ports": [{"hostPort": 8000}],
	}]}}}})
	some m_auth in k8s.deny with input as bad_port
	contains(m_auth, "VLLM_API_KEY")
	some m_hp in k8s.deny with input as bad_port
	contains(m_hp, "hostPort")

	bad_svc_ext := {
		"apiVersion": "v1",
		"kind": "Service",
		"metadata": {"name": "vllm-ext"},
		"spec": {"type": "ClusterIP", "externalIPs": ["203.0.113.10"]},
	}
	some m_ext in k8s.deny with input as bad_svc_ext
	contains(m_ext, "externalIPs")

	empty_auth := object.union(base_deploy, {"spec": {"template": {"spec": {"containers": [{
		"name": "vllm",
		"image": pinned_img,
		"args": ["--allowed-local-media-path", "/"],
		"env": [{"name": "VLLM_API_KEY", "value": ""}],
		"resources": {"limits": {"memory": "16Gi"}},
		"securityContext": {
			"procMount": "Unmasked",
			"allowPrivilegeEscalation": false,
			"readOnlyRootFilesystem": true,
			"capabilities": {"drop": ["ALL"], "add": ["NET_ADMIN"]},
		},
	}]}}}})
	some m_empty in k8s.deny with input as empty_auth
	contains(m_empty, "VLLM_API_KEY")
	some m_lfi in k8s.deny with input as empty_auth
	contains(m_lfi, "--allowed-local-media-path")
	some m_pm in k8s.deny with input as empty_auth
	contains(m_pm, "procMount=Unmasked")
	some m_cap in k8s.deny with input as empty_auth
	contains(m_cap, "NET_ADMIN")
}

test_deny_host_escape_surfaces if {
	bad := object.union(base_deploy, {"spec": {"template": {"spec": {
		"hostNetwork": true,
		"hostPID": true,
		"volumes": [{"name": "sock", "hostPath": {"path": "/var/run/docker.sock"}}],
	}}}})
	some m1 in k8s.deny with input as bad
	contains(m1, "hostNetwork=true")
	some m2 in k8s.deny with input as bad
	contains(m2, "hostPID=true")
	some m3 in k8s.deny with input as bad
	contains(m3, "mounts hostPath")
}

test_deny_pss_restricted_and_limits_gaps if {
	bad := {
		"apiVersion": "apps/v1",
		"kind": "Deployment",
		"metadata": {"name": "unsafe-deploy"},
		"spec": {"template": {"spec": {"containers": [{
			"name": "vllm",
			"image": pinned_img,
			"securityContext": {},
		}]}}},
	}
	some m_root in k8s.deny with input as bad
	contains(m_root, "runAsNonRoot=true")
	some m_sec in k8s.deny with input as bad
	contains(m_sec, "seccompProfile")
	some m_ro in k8s.deny with input as bad
	contains(m_ro, "readOnlyRootFilesystem=true")
	some m_lim in k8s.deny with input as bad
	contains(m_lim, "resources.limits.memory")
	some m_sa in k8s.deny with input as bad
	contains(m_sa, "automountServiceAccountToken=false")
}
