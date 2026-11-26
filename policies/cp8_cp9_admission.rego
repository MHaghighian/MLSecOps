# MLSecOps reference admission policy: bind CP8 release approval to CP9 deploy integrity,
# enforce blocking gates (CP4/CP7/CP8), cross-check CycloneDX component hashes, guard data/telemetry/DMR,
# and enforce OWASP Agentic-MCP / KV controls.
# Uses Conftest's default `package main` so `conftest test --policy policies <file>` evaluates rules out of the box.
package main

import rego.v1

default allow := false

allow if {
	count(deny) == 0
}

has_non_empty_text(root_obj, keys) if {
	val := object.get(root_obj, keys, "")
	is_string(val)
	count(trim_space(val)) > 0
}

is_sha256_prefixed(val) if {
	is_string(val)
	regex.match("^sha256:[a-f0-9]{64}$", val)
}

is_sha256_hex(val) if {
	is_string(val)
	regex.match("^[a-f0-9]{64}$", val)
}

# Metadata & ownership sanity (fail closed if omitted).
deny contains msg if {
	not has_non_empty_text(input, ["metadata", "systemScope"])
	msg := "CRITICAL [Metadata]: missing or empty metadata.systemScope"
}

deny contains msg if {
	not has_non_empty_text(input, ["metadata", "sharedResponsibilityRecord", "modelOwner"])
	msg := "HIGH [Metadata]: missing sharedResponsibilityRecord.modelOwner"
}

deny contains msg if {
	not has_non_empty_text(input, ["metadata", "sharedResponsibilityRecord", "platformOwner"])
	msg := "HIGH [Metadata]: missing sharedResponsibilityRecord.platformOwner"
}

deny contains msg if {
	not has_non_empty_text(input, ["metadata", "sharedResponsibilityRecord", "socOwner"])
	msg := "HIGH [Metadata]: missing sharedResponsibilityRecord.socOwner"
}

# Blocking release decisions: CP4 (Data/RAG ACL), CP7 (Security Validation), CP8 (Release Decision).
deny contains msg if {
	not input.lifecycleControlGates.cp4_dataAndRagAclGate.status == "PASS"
	msg := "CRITICAL [CP4]: data/RAG ACL gate status is not PASS"
}

deny contains msg if {
	input.dataProvenance.piiScanResult == "FAIL"
	msg := "CRITICAL [CP4/Ch.4]: dataProvenance.piiScanResult is FAIL"
}

deny contains msg if {
	has_non_empty_text(input, ["dataProvenance", "vectorIndexVersionHash"])
	input.dataProvenance.backupRevocationVerified == false
	msg := "HIGH [Ch.4/Ch.7]: RAG vector index backup/snapshot revocation verification failed"
}

deny contains msg if {
	not input.lifecycleControlGates.cp7_adversarialAndRedTeamGate.status == "PASS"
	msg := "CRITICAL [CP7]: security validation gate status is not PASS"
}

deny contains msg if {
	score := input.lifecycleControlGates.cp7_adversarialAndRedTeamGate.agentMisalignmentScore
	score > 0.15
	msg := sprintf("HIGH [CP7/Ch.8]: agentMisalignmentScore %v exceeds 0.15 release threshold", [score])
}

deny contains msg if {
	input.metadata.systemScope in {"LLM-RAG", "Agentic-MCP"}
	phases := input.lifecycleControlGates.cp7_adversarialAndRedTeamGate.redTeamPhasesCompleted
	phases < 4
	msg := sprintf("HIGH [CP7/Ch.12]: redTeamPhasesCompleted (%v) below minimum 4 phases", [phases])
}

deny contains msg if {
	not input.lifecycleControlGates.cp8_releaseDecisionGate.decision == "APPROVED"
	msg := "CRITICAL [CP8]: release decision is not APPROVED"
}

# CP8 → CP9 TOCTOU: boundToCp9Digest must be a valid sha256 digest across all scopes.
deny contains msg if {
	not has_non_empty_text(input, ["lifecycleControlGates", "cp8_releaseDecisionGate", "boundToCp9Digest"])
	msg := "CRITICAL [CP8->CP9]: missing cp8_releaseDecisionGate.boundToCp9Digest"
}

deny contains msg if {
	has_non_empty_text(input, ["lifecycleControlGates", "cp8_releaseDecisionGate", "boundToCp9Digest"])
	approved := input.lifecycleControlGates.cp8_releaseDecisionGate.boundToCp9Digest
	not is_sha256_prefixed(approved)
	msg := sprintf("CRITICAL [CP8->CP9]: boundToCp9Digest %v is not a valid sha256:<64-hex> digest", [approved])
}

# Non-managed scopes must present a valid sha256 modelArtifact digest matching CP8 approval.
deny contains msg if {
	has_non_empty_text(input, ["metadata", "systemScope"])
	input.metadata.systemScope != "Managed-API"
	not has_non_empty_text(input, ["modelArtifact", "sha256Digest"])
	msg := "CRITICAL [CP9]: missing modelArtifact.sha256Digest for non-managed deployment"
}

deny contains msg if {
	has_non_empty_text(input, ["metadata", "systemScope"])
	input.metadata.systemScope != "Managed-API"
	has_non_empty_text(input, ["modelArtifact", "sha256Digest"])
	deployed := input.modelArtifact.sha256Digest
	not is_sha256_prefixed(deployed)
	msg := sprintf("CRITICAL [CP9]: modelArtifact.sha256Digest %v is not a valid sha256:<64-hex> digest", [deployed])
}

deny contains msg if {
	has_non_empty_text(input, ["metadata", "systemScope"])
	input.metadata.systemScope != "Managed-API"
	approved := input.lifecycleControlGates.cp8_releaseDecisionGate.boundToCp9Digest
	deployed := input.modelArtifact.sha256Digest
	is_sha256_prefixed(approved)
	is_sha256_prefixed(deployed)
	approved != deployed
	msg := sprintf("CRITICAL [CP8->CP9]: model digest %v does not match CP8-approved digest %v", [deployed, approved])
}

# Managed-API scopes bind CP8 approval to managedApiConfig.configSnapshotHash instead of model weights.
deny contains msg if {
	input.metadata.systemScope == "Managed-API"
	not has_non_empty_text(input, ["managedApiConfig", "configSnapshotHash"])
	msg := "CRITICAL [CP9]: missing managedApiConfig.configSnapshotHash for Managed-API deployment"
}

deny contains msg if {
	input.metadata.systemScope == "Managed-API"
	has_non_empty_text(input, ["managedApiConfig", "configSnapshotHash"])
	deployed := input.managedApiConfig.configSnapshotHash
	not is_sha256_prefixed(deployed)
	msg := sprintf("CRITICAL [CP9]: managedApiConfig.configSnapshotHash %v is not a valid sha256:<64-hex> digest", [deployed])
}

deny contains msg if {
	input.metadata.systemScope == "Managed-API"
	approved := input.lifecycleControlGates.cp8_releaseDecisionGate.boundToCp9Digest
	deployed := input.managedApiConfig.configSnapshotHash
	is_sha256_prefixed(approved)
	is_sha256_prefixed(deployed)
	approved != deployed
	msg := sprintf("CRITICAL [CP8->CP9]: managed config digest %v does not match CP8-approved digest %v", [deployed, approved])
}

# CP9 cryptographic/configuration provenance must be verified with a real method (no none/n/a placeholder).
deny contains msg if {
	not input.cryptographicProvenance.cp9_checkpointVerified == true
	msg := "CRITICAL [CP9]: integrity/provenance checkpoint not verified"
}

deny contains msg if {
	not has_non_empty_text(input, ["cryptographicProvenance", "signatureMethod"])
	msg := "CRITICAL [CP9]: missing cryptographicProvenance.signatureMethod"
}

deny contains msg if {
	method := object.get(input, ["cryptographicProvenance", "signatureMethod"], "")
	is_string(method)
	lower(trim_space(method)) in {"none", "n/a", "na", "null", "tbd"}
	msg := sprintf("CRITICAL [CP9]: placeholder cryptographicProvenance.signatureMethod %v is not permitted", [method])
}

# Ch.5: refuse artifacts flagged unreadable/obfuscated (case-insensitive) or weak BOM hashes / component drift.
deny contains msg if {
	some component in input.components
	some prop in component.properties
	prop.name == "aisbom:unreadable"
	lower(trim_space(prop.value)) == "true"
	msg := sprintf("CRITICAL [Ch.5]: unreadable or obfuscated binary header on component %v", [component.name])
}

deny contains msg if {
	input.lifecycleControlGates.cp7_adversarialAndRedTeamGate.unreadableArtifactsDetected == true
	msg := "CRITICAL [Ch.5/CP7]: unreadableArtifactsDetected is true"
}

deny contains msg if {
	some component in input.components
	some h in component.hashes
	upper(trim_space(h.alg)) in {"MD5", "SHA-1", "SHA1"}
	msg := sprintf("HIGH [Ch.5/CP9]: weak hash algorithm %v on component %v; use SHA-256+", [h.alg, component.name])
}

deny contains msg if {
	has_non_empty_text(input, ["metadata", "systemScope"])
	input.metadata.systemScope != "Managed-API"
	is_sha256_prefixed(input.modelArtifact.sha256Digest)
	some component in input.components
	component.type == "machine-learning-model"
	some h in component.hashes
	upper(trim_space(h.alg)) == "SHA-256"
	expected := trim_prefix(input.modelArtifact.sha256Digest, "sha256:")
	lower(h.content) != expected
	msg := sprintf("CRITICAL [Ch.5/CP9]: ML component %v SHA-256 (%v) does not match modelArtifact digest (%v)", [component.name, h.content, expected])
}

# Appendix E.1.7: local OCI runner TCP endpoint must not be exposed without network isolation.
deny contains msg if {
	input.localRunnerConfig.tcpHostExposed == true
	not input.localRunnerConfig.networkIsolated == true
	msg := "CRITICAL [E.1.7]: localRunnerConfig exposes TCP endpoint without network isolation"
}

# Ch.4/10: privacy-aware telemetry must disable raw prompt logging by default.
deny contains msg if {
	input.runtimeTelemetry.rawPromptLoggingDisabled == false
	msg := "HIGH [Ch.4/10]: runtimeTelemetry.rawPromptLoggingDisabled must not be false"
}

# Ch.8: MCP09 — refuse unpinned, whitespace/case-shadowed, cleartext/SSRF, or drifted MCP servers.
deny contains msg if {
	some tool in input.runtimeAgentConfig.mcpTools
	hashes := object.get(input, ["cryptographicProvenance", "mcpSchemaHashes"], {})
	server := object.get(tool, "serverName", "")
	not has_non_empty_text(hashes, [server])
	msg := sprintf("CRITICAL [Ch.8 MCP09]: unpinned MCP server %v missing from mcpSchemaHashes", [object.get(tool, "serverName", "<unnamed>")])
}

deny contains msg if {
	some i, t1 in input.runtimeAgentConfig.mcpTools
	some j, t2 in input.runtimeAgentConfig.mcpTools
	i < j
	lower(trim_space(t1.serverName)) == lower(trim_space(t2.serverName))
	msg := sprintf("HIGH [Ch.8 MCP09]: duplicate or whitespace/case-conflicting MCP serverName %v", [t2.serverName])
}

deny contains msg if {
	some tool in input.runtimeAgentConfig.mcpTools
	not has_non_empty_text(tool, ["currentSchemaHash"])
	msg := sprintf("CRITICAL [Ch.8 MCP]: missing currentSchemaHash for MCP server %v", [object.get(tool, "serverName", "<unnamed>")])
}

deny contains msg if {
	some tool in input.runtimeAgentConfig.mcpTools
	hashes := object.get(input, ["cryptographicProvenance", "mcpSchemaHashes"], {})
	server := object.get(tool, "serverName", "")
	has_non_empty_text(hashes, [server])
	pinned := hashes[server]
	not is_sha256_hex(pinned)
	msg := sprintf("CRITICAL [Ch.8 MCP]: pinned mcpSchemaHashes[%v] is not a valid 64-hex SHA-256 hash", [server])
}

deny contains msg if {
	some tool in input.runtimeAgentConfig.mcpTools
	has_non_empty_text(tool, ["currentSchemaHash"])
	current := tool.currentSchemaHash
	not is_sha256_hex(current)
	msg := sprintf("CRITICAL [Ch.8 MCP]: currentSchemaHash for server %v is not a valid 64-hex SHA-256 hash", [object.get(tool, "serverName", "<unnamed>")])
}

deny contains msg if {
	some tool in input.runtimeAgentConfig.mcpTools
	pinned := input.cryptographicProvenance.mcpSchemaHashes[tool.serverName]
	is_sha256_hex(pinned)
	is_sha256_hex(tool.currentSchemaHash)
	tool.currentSchemaHash != pinned
	msg := sprintf("CRITICAL [Ch.8 MCP]: schema hash drift for server %v", [tool.serverName])
}

deny contains msg if {
	some tool in input.runtimeAgentConfig.mcpTools
	lower(object.get(tool, "transport", "")) in {"http", "ws"}
	endpoint := lower(object.get(tool, "endpoint", ""))
	not regex.match("^https?://(localhost|127\\.0\\.0\\.1)(:|/|$)", endpoint)
	msg := sprintf("CRITICAL [Ch.8 MCP]: remote MCP server %v uses cleartext transport %v", [tool.serverName, tool.transport])
}

deny contains msg if {
	some tool in input.runtimeAgentConfig.mcpTools
	endpoint := lower(object.get(tool, "endpoint", ""))
	regex.match("(169\\.254\\.169\\.254|100\\.100\\.100\\.200|metadata\\.google\\.internal)", endpoint)
	msg := sprintf("CRITICAL [Ch.8 MCP SSRF]: MCP server %v targets cloud metadata endpoint", [tool.serverName])
}

# Ch.8 (OWASP ASI02/ASI03/ASI06 & MCP Sampling): kill-switch, scoped creds, Intent Gate, memory provenance, sampling cap.
deny contains msg if {
	input.metadata.systemScope == "Agentic-MCP"
	not input.runtimeAgentConfig.killSwitchEnabled == true
	msg := "HIGH [Ch.8]: Agentic-MCP deploy requires killSwitchEnabled=true"
}

deny contains msg if {
	input.metadata.systemScope == "Agentic-MCP"
	not input.runtimeAgentConfig.scopedCredentialsRequired == true
	msg := "HIGH [Ch.8]: Agentic-MCP deploy requires scopedCredentialsRequired=true"
}

deny contains msg if {
	input.metadata.systemScope == "Agentic-MCP"
	not input.runtimeAgentConfig.intentGateEnabled == true
	msg := "HIGH [Ch.8 ASI02/ASI03]: Agentic-MCP deploy requires intentGateEnabled=true"
}

deny contains msg if {
	input.runtimeAgentConfig.memoryStoreEnabled == true
	not input.runtimeAgentConfig.memoryProvenanceVerified == true
	msg := "HIGH [Ch.8 ASI06]: persistent agent memory requires memoryProvenanceVerified=true"
}

deny contains msg if {
	input.runtimeAgentConfig.samplingEnabled == true
	not input.runtimeAgentConfig.samplingBudgetCapped == true
	msg := "HIGH [Ch.8 MCP]: MCP samplingEnabled requires samplingBudgetCapped=true"
}

# Ch.7/16: cross-model KV reuse without an alignment/isolation control (fail closed if omitted).
deny contains msg if {
	input.inferenceConfig.crossModelKvCacheReuse == true
	not input.inferenceConfig.kvAlignmentControlActive == true
	not input.inferenceConfig.tenantKvPartitioned == true
	msg := "HIGH [Ch.7/16]: cross-model KV cache reuse requires alignment control or tenant partition evidence"
}
