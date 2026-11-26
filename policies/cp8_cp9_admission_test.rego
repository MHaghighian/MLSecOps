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
			"redTeamPhasesCompleted": 6,
			"agentMisalignmentScore": 0.03,
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
		"intentGateEnabled": true,
		"memoryStoreEnabled": true,
		"memoryProvenanceVerified": true,
		"samplingEnabled": false,
		"mcpTools": [{
			"serverName": "payments-mcp",
			"transport": "https",
			"endpoint": "https://mcp.internal.example/payments",
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
		"cryptographicProvenance": {"signatureMethod": "managed-config-snapshot"},
		"managedApiConfig": {"configSnapshotHash": digest_a},
	})
	main.allow with input as pack
}

test_deny_missing_system_scope if {
	pack := json.remove(base_pack, ["metadata/systemScope"])
	not main.allow with input as pack
	"CRITICAL [Metadata]: missing or empty metadata.systemScope" in main.deny with input as pack
}

test_deny_missing_owner_metadata if {
	pack := object.union(base_pack, {"metadata": {"sharedResponsibilityRecord": {"socOwner": "  "}}})
	not main.allow with input as pack
	"HIGH [Metadata]: missing sharedResponsibilityRecord.socOwner" in main.deny with input as pack
}

test_deny_cp4_and_pii_and_backup_revocation if {
	pack := object.union(base_pack, {
		"lifecycleControlGates": {"cp4_dataAndRagAclGate": {"status": "BLOCK"}},
		"dataProvenance": {
			"piiScanResult": "FAIL",
			"vectorIndexVersionHash": digest_a,
			"backupRevocationVerified": false,
		},
	})
	not main.allow with input as pack
	"CRITICAL [CP4]: data/RAG ACL gate status is not PASS" in main.deny with input as pack
	"CRITICAL [CP4/Ch.4]: dataProvenance.piiScanResult is FAIL" in main.deny with input as pack
	"HIGH [Ch.4/Ch.7]: RAG vector index backup/snapshot revocation verification failed" in main.deny with input as pack
}

test_deny_cp7_thresholds_and_block if {
	pack := object.union(base_pack, {"lifecycleControlGates": {"cp7_adversarialAndRedTeamGate": {
		"status": "BLOCK",
		"redTeamPhasesCompleted": 2,
		"agentMisalignmentScore": 0.42,
	}}})
	not main.allow with input as pack
	"CRITICAL [CP7]: security validation gate status is not PASS" in main.deny with input as pack
	some m1 in main.deny with input as pack
	contains(m1, "HIGH [CP7/Ch.8]: agentMisalignmentScore")
	some m2 in main.deny with input as pack
	contains(m2, "HIGH [CP7/Ch.12]: redTeamPhasesCompleted")
}

test_deny_cp8_cp9_digest_failures if {
	missing_bound := json.remove(base_pack, ["lifecycleControlGates/cp8_releaseDecisionGate/boundToCp9Digest"])
	"CRITICAL [CP8->CP9]: missing cp8_releaseDecisionGate.boundToCp9Digest" in main.deny with input as missing_bound

	bad_fmt := object.union(base_pack, {
		"modelArtifact": {"sha256Digest": "latest"},
		"lifecycleControlGates": {"cp8_releaseDecisionGate": {"boundToCp9Digest": "latest"}},
	})
	some fmt_msg in main.deny with input as bad_fmt
	contains(fmt_msg, "is not a valid sha256:<64-hex> digest")

	mismatch := object.union(base_pack, {"modelArtifact": {"sha256Digest": digest_b}})
	some m_msg in main.deny with input as mismatch
	startswith(m_msg, "CRITICAL [CP8->CP9]: model digest")

	managed_mismatch := object.union(base_pack, {
		"metadata": {"systemScope": "Managed-API"},
		"managedApiConfig": {"configSnapshotHash": digest_b},
	})
	some mg_msg in main.deny with input as managed_mismatch
	startswith(mg_msg, "CRITICAL [CP8->CP9]: managed config digest")
}

test_deny_missing_digests_per_scope if {
	nm_missing := json.remove(base_pack, ["modelArtifact/sha256Digest"])
	"CRITICAL [CP9]: missing modelArtifact.sha256Digest for non-managed deployment" in main.deny with input as nm_missing

	mg_missing := object.union(base_pack, {"metadata": {"systemScope": "Managed-API"}})
	"CRITICAL [CP9]: missing managedApiConfig.configSnapshotHash for Managed-API deployment" in main.deny with input as mg_missing
}

test_deny_provenance_and_signature_placeholder if {
	bad := object.union(base_pack, {
		"lifecycleControlGates": {"cp8_releaseDecisionGate": {"decision": "REJECTED"}},
		"cryptographicProvenance": {"cp9_checkpointVerified": false, "signatureMethod": "N/A"},
	})
	"CRITICAL [CP8]: release decision is not APPROVED" in main.deny with input as bad
	"CRITICAL [CP9]: integrity/provenance checkpoint not verified" in main.deny with input as bad
	some m in main.deny with input as bad
	contains(m, "placeholder cryptographicProvenance.signatureMethod")
}

test_deny_supply_chain_components_and_case_unreadable if {
	bad := object.union(base_pack, {"components": [{
		"name": "bad.safetensors",
		"type": "machine-learning-model",
		"hashes": [
			{"alg": "MD5", "content": "deadbeef"},
			{"alg": "SHA-256", "content": hash_b},
		],
		"properties": [{"name": "aisbom:unreadable", "value": "TRUE"}],
	}]})
	some m1 in main.deny with input as bad
	contains(m1, "CRITICAL [Ch.5]: unreadable")
	some m2 in main.deny with input as bad
	contains(m2, "HIGH [Ch.5/CP9]: weak hash algorithm")
	some m3 in main.deny with input as bad
	contains(m3, "CRITICAL [Ch.5/CP9]: no machine-learning-model component SHA-256 matches modelArtifact digest")

	# Multi-model BOMs (primary LLM matching modelArtifact + companion embedding model) must pass cleanly.
	multi_ok := object.union(base_pack, {"components": [
		{"name": "primary-llm", "type": "machine-learning-model", "hashes": [{"alg": "SHA-256", "content": hash_a}]},
		{"name": "embedding-bge", "type": "machine-learning-model", "hashes": [{"alg": "SHA-256", "content": hash_b}]},
	]})
	main.allow with input as multi_ok
}

test_deny_dmr_exposed_and_raw_prompt_telemetry if {
	bad := object.union(base_pack, {
		"localRunnerConfig": {"tcpHostExposed": true, "networkIsolated": false},
		"runtimeTelemetry": {"rawPromptLoggingDisabled": false},
	})
	"CRITICAL [E.1.7]: localRunnerConfig exposes TCP endpoint without network isolation" in main.deny with input as bad
	"HIGH [Ch.4/10]: runtimeTelemetry.rawPromptLoggingDisabled must not be false" in main.deny with input as bad
}

test_deny_mcp_security_controls if {
	bad := object.union(base_pack, {"runtimeAgentConfig": {"mcpTools": [
		{"serverName": "payments-mcp", "transport": "http", "endpoint": "http://169.254.169.254/latest", "currentSchemaHash": hash_b},
		{"serverName": "PAYMENTS-MCP ", "transport": "https", "endpoint": "https://x.example", "currentSchemaHash": "bad"},
		{"serverName": "shadow-mcp", "currentSchemaHash": hash_a},
	]}})
	some m1 in main.deny with input as bad
	contains(m1, "CRITICAL [Ch.8 MCP09]: unpinned MCP server shadow-mcp")
	some m2 in main.deny with input as bad
	contains(m2, "HIGH [Ch.8 MCP09]: duplicate or whitespace/case-conflicting")
	some m3 in main.deny with input as bad
	contains(m3, "CRITICAL [Ch.8 MCP]: schema hash drift for server payments-mcp")
	some m4 in main.deny with input as bad
	contains(m4, "CRITICAL [Ch.8 MCP]: remote MCP server payments-mcp uses cleartext transport")
	some m5 in main.deny with input as bad
	contains(m5, "CRITICAL [Ch.8 MCP SSRF]")
}

test_deny_agentic_asi_and_sampling_and_kv if {
	bad := object.union(base_pack, {
		"inferenceConfig": {"crossModelKvCacheReuse": true, "kvAlignmentControlActive": false, "tenantKvPartitioned": false},
		"runtimeAgentConfig": {
			"killSwitchEnabled": false,
			"scopedCredentialsRequired": false,
			"intentGateEnabled": false,
			"memoryStoreEnabled": true,
			"memoryProvenanceVerified": false,
			"samplingEnabled": true,
			"samplingBudgetCapped": false,
		},
	})
	"HIGH [Ch.8]: Agentic-MCP deploy requires killSwitchEnabled=true" in main.deny with input as bad
	"HIGH [Ch.8]: Agentic-MCP deploy requires scopedCredentialsRequired=true" in main.deny with input as bad
	"HIGH [Ch.8 ASI02/ASI03]: Agentic-MCP deploy requires intentGateEnabled=true" in main.deny with input as bad
	"HIGH [Ch.8 ASI06]: persistent agent memory requires memoryProvenanceVerified=true" in main.deny with input as bad
	"HIGH [Ch.8 MCP]: MCP samplingEnabled requires samplingBudgetCapped=true" in main.deny with input as bad
	some mkv in main.deny with input as bad
	contains(mkv, "HIGH [Ch.7/16]: cross-model KV cache reuse")
}
