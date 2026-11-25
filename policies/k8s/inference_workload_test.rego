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
				"securityContext": {"runAsNonRoot": true},
				"containers": [{
					"name": "vllm",
					"image": pinned_img,
					"securityContext": {
						"allowPrivilegeEscalation": false,
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

test_deny_unpinned_image_tag if {
	bad := object.union(base_deploy, {"spec": {"template": {"spec": {"containers": [{
		"name": "vllm",
		"image": "vllm/vllm-openai:latest",
		"securityContext": {
			"allowPrivilegeEscalation": false,
			"capabilities": {"drop": ["ALL"]},
		},
	}]}}}})
	some msg in k8s.deny with input as bad
	contains(msg, "CRITICAL [Ch.16/CP9]: container")
}

test_deny_missing_non_root_and_sa_token if {
	bad := json.remove(base_deploy, [
		"spec/template/spec/securityContext/runAsNonRoot",
		"spec/template/spec/automountServiceAccountToken",
	])
	"HIGH [Ch.16]: Deployment \"llm-inference\" must enforce securityContext.runAsNonRoot=true" in k8s.deny with input as bad
	"HIGH [Ch.16]: Deployment \"llm-inference\" must set automountServiceAccountToken=false on inference workloads" in k8s.deny with input as bad
}

test_deny_privilege_escalation_and_missing_cap_drop if {
	bad := object.union(base_deploy, {"spec": {"template": {"spec": {"containers": [{
		"name": "vllm",
		"image": pinned_img,
		"securityContext": {},
	}]}}}})
	"HIGH [Ch.16]: container \"vllm\" must set securityContext.allowPrivilegeEscalation=false" in k8s.deny with input as bad
	"HIGH [Ch.16]: container \"vllm\" must drop ALL capabilities" in k8s.deny with input as bad
}
