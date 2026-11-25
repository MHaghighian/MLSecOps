package main_test

import data.main
import rego.v1

digest_a := "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

digest_b := "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

hash_a := "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

hash_b := "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

base_pack := {
	"bomFormat": "CycloneDX",
	"specVersion": "1.6",
	"version": 1,
	"metadata": {
		"timestamp": "2026-11-03T00:00:00Z",
		"systemScope": "Agentic-MCP",
		"sharedResponsibilityRecord": {
			"modelOwner": "ml",
			"platformOwner": "platform",
			"socOwner": "soc",
		},
	},
	"modelArtifact": {"sha256Digest": digest_a},
	"components": [],
	"lifecycleControlGates": {
		"cp4_dataAndRagAclGate": {"status": "PASS"},
		"cp7_adversarialAndRedTeamGate": {
			"status": "PASS",
			"unreadableArtifactsDetected": false,
		},
		"cp8_releaseDecisionGate": {
			"decision": "APPROVED",
			"approverRole": "release-owner",
			"boundToCp9Digest": digest_a,
		},
	},
	"cryptographicProvenance": {
		"cp9_checkpointVerified": true,
		"signatureMethod": "sigstore-cosign",
		"mcpSchemaHashes": {"payments-mcp": hash_a},
	},
	"inferenceConfig": {
		"crossModelKvCacheReuse": false,
		"kvAlignmentControlActive": false,
		"tenantKvPartitioned": true,
	},
	"runtimeAgentConfig": {
		"killSwitchEnabled": true,
		"scopedCredentialsRequired": true,
		"mcpTools": [{
			"serverName": "payments-mcp",
			"currentSchemaHash": hash_a,
		}],
	},
}

test_valid_agentic_mcp_allows if {
	main.allow with input as base_pack
	count(main.deny) == 0 with input as base_pack
}

test_valid_managed_api_allows if {
	pack := object.union(base_pack, {
		"metadata": {"systemScope": "Managed-API"},
		"managedApiConfig": {"configSnapshotHash": digest_a},
	})
	main.allow with input as pack
}

test_deny_missing_system_scope if {
	pack := json.remove(base_pack, ["metadata/systemScope"])
	not main.allow with input as pack
	"CRITICAL [Metadata]: missing or empty metadata.systemScope" in main.deny with input as pack
}

test_deny_empty_system_scope if {
	pack := object.union(base_pack, {"metadata": {"systemScope": "   "}})
	not main.allow with input as pack
	"CRITICAL [Metadata]: missing or empty metadata.systemScope" in main.deny with input as pack
}

test_deny_missing_bound_to_cp9_digest if {
	pack := json.remove(base_pack, ["lifecycleControlGates/cp8_releaseDecisionGate/boundToCp9Digest"])
	not main.allow with input as pack
	"CRITICAL [CP8->CP9]: missing cp8_releaseDecisionGate.boundToCp9Digest" in main.deny with input as pack
}

test_deny_non_managed_missing_model_digest if {
	pack := json.remove(base_pack, ["modelArtifact/sha256Digest"])
	not main.allow with input as pack
	"CRITICAL [CP9]: missing modelArtifact.sha256Digest for non-managed deployment" in main.deny with input as pack
}

test_deny_non_managed_digest_mismatch if {
	pack := object.union(base_pack, {"modelArtifact": {"sha256Digest": digest_b}})
	not main.allow with input as pack
	some msg in main.deny with input as pack
	startswith(msg, "CRITICAL [CP8->CP9]: model digest")
}

test_deny_managed_api_missing_config_hash if {
	pack := object.union(base_pack, {"metadata": {"systemScope": "Managed-API"}})
	not main.allow with input as pack
	"CRITICAL [CP9]: missing managedApiConfig.configSnapshotHash for Managed-API deployment" in main.deny with input as pack
}

test_deny_managed_api_digest_mismatch if {
	pack := object.union(base_pack, {
		"metadata": {"systemScope": "Managed-API"},
		"managedApiConfig": {"configSnapshotHash": digest_b},
	})
	not main.allow with input as pack
	some msg in main.deny with input as pack
	startswith(msg, "CRITICAL [CP8->CP9]: managed config digest")
}

test_deny_cp8_not_approved if {
	pack := object.union(base_pack, {"lifecycleControlGates": {"cp8_releaseDecisionGate": {"decision": "REJECTED"}}})
	not main.allow with input as pack
	"CRITICAL [CP8]: release decision is not APPROVED" in main.deny with input as pack
}

test_deny_cp9_not_verified if {
	pack := json.remove(base_pack, ["cryptographicProvenance/cp9_checkpointVerified"])
	not main.allow with input as pack
	"CRITICAL [CP9]: integrity/provenance checkpoint not verified" in main.deny with input as pack
}

test_deny_unreadable_component if {
	pack := object.union(base_pack, {"components": [{
		"name": "bad.safetensors",
		"properties": [{"name": "aisbom:unreadable", "value": "true"}],
	}]})
	not main.allow with input as pack
	some msg in main.deny with input as pack
	contains(msg, "CRITICAL [Ch.5]: unreadable")
}

test_deny_cp7_unreadable_artifacts if {
	pack := object.union(base_pack, {"lifecycleControlGates": {"cp7_adversarialAndRedTeamGate": {"unreadableArtifactsDetected": true}}})
	not main.allow with input as pack
	"CRITICAL [Ch.5/CP7]: unreadableArtifactsDetected is true" in main.deny with input as pack
}

test_deny_unpinned_mcp09 if {
	pack := object.union(base_pack, {"runtimeAgentConfig": {"mcpTools": [{
		"serverName": "shadow-mcp",
		"currentSchemaHash": hash_a,
	}]}})
	not main.allow with input as pack
	some msg in main.deny with input as pack
	contains(msg, "CRITICAL [Ch.8 MCP09]: unpinned MCP server shadow-mcp")
}

test_deny_missing_mcp_current_schema_hash if {
	pack := object.union(base_pack, {"runtimeAgentConfig": {"mcpTools": [{"serverName": "payments-mcp"}]}})
	not main.allow with input as pack
	some msg in main.deny with input as pack
	contains(msg, "CRITICAL [Ch.8 MCP]: missing currentSchemaHash")
}

test_deny_mcp_schema_drift if {
	pack := object.union(base_pack, {"runtimeAgentConfig": {"mcpTools": [{
		"serverName": "payments-mcp",
		"currentSchemaHash": hash_b,
	}]}})
	not main.allow with input as pack
	some msg in main.deny with input as pack
	contains(msg, "CRITICAL [Ch.8 MCP]: schema hash drift for server payments-mcp")
}

test_deny_agentic_missing_kill_switch if {
	pack := json.remove(base_pack, ["runtimeAgentConfig/killSwitchEnabled"])
	not main.allow with input as pack
	"HIGH [Ch.8]: Agentic-MCP deploy requires killSwitchEnabled=true" in main.deny with input as pack
}

test_deny_agentic_missing_scoped_credentials if {
	pack := json.remove(base_pack, ["runtimeAgentConfig/scopedCredentialsRequired"])
	not main.allow with input as pack
	"HIGH [Ch.8]: Agentic-MCP deploy requires scopedCredentialsRequired=true" in main.deny with input as pack
}

test_deny_cross_model_kv_reuse_unguarded if {
	pack := object.union(base_pack, {"inferenceConfig": {
		"crossModelKvCacheReuse": true,
		"kvAlignmentControlActive": false,
		"tenantKvPartitioned": false,
	}})
	not main.allow with input as pack
	some msg in main.deny with input as pack
	contains(msg, "HIGH [Ch.7/16]: cross-model KV cache reuse")
}

test_allow_cross_model_kv_reuse_when_aligned if {
	pack := object.union(base_pack, {"inferenceConfig": {
		"crossModelKvCacheReuse": true,
		"kvAlignmentControlActive": true,
		"tenantKvPartitioned": false,
	}})
	main.allow with input as pack
}
