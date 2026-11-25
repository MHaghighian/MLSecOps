# MLSecOps reference admission policy: bind CP8 release approval to CP9 deploy integrity,
# enforce blocking gates (CP4/CP7/CP8), validate SHA-256 formats, and guard Agentic-MCP/KV controls.
# Uses Conftest's default `package main` so `conftest test --policy policies <file>` evaluates rules out of the box.
# Input: Evidence Pack JSON (see schemas/evidence-pack.schema.json).
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

# Metadata scope must always be declared (fail closed if omitted).
deny contains msg if {
	not has_non_empty_text(input, ["metadata", "systemScope"])
	msg := "CRITICAL [Metadata]: missing or empty metadata.systemScope"
}

# Level 2+ blocking release decisions: CP4 (Data/RAG ACL), CP7 (Security Validation), CP8 (Release Decision).
deny contains msg if {
	not input.lifecycleControlGates.cp4_dataAndRagAclGate.status == "PASS"
	msg := "CRITICAL [CP4]: data/RAG ACL gate status is not PASS"
}

deny contains msg if {
	not input.lifecycleControlGates.cp7_adversarialAndRedTeamGate.status == "PASS"
	msg := "CRITICAL [CP7]: security validation gate status is not PASS"
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
	approved := object.get(input, ["lifecycleControlGates", "cp8_releaseDecisionGate", "boundToCp9Digest"], "")
	is_string(approved)
	count(trim_space(approved)) > 0
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
	deployed := object.get(input, ["modelArtifact", "sha256Digest"], "")
	is_string(deployed)
	count(trim_space(deployed)) > 0
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
	deployed := object.get(input, ["managedApiConfig", "configSnapshotHash"], "")
	is_string(deployed)
	count(trim_space(deployed)) > 0
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

# CP9 cryptographic/configuration provenance must be verified with a concrete method (no none/n/a placeholder).
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

# Ch.5: refuse artifacts flagged unreadable / obfuscated by binary scanners.
deny contains msg if {
	some component in input.components
	some prop in component.properties
	prop.name == "aisbom:unreadable"
	prop.value == "true"
	msg := sprintf("CRITICAL [Ch.5]: unreadable or obfuscated binary header on component %v", [component.name])
}

deny contains msg if {
	input.lifecycleControlGates.cp7_adversarialAndRedTeamGate.unreadableArtifactsDetected == true
	msg := "CRITICAL [Ch.5/CP7]: unreadableArtifactsDetected is true"
}

# Ch.8: MCP09 — refuse any runtime MCP server absent from pinned mcpSchemaHashes.
deny contains msg if {
	some tool in input.runtimeAgentConfig.mcpTools
	hashes := object.get(input, ["cryptographicProvenance", "mcpSchemaHashes"], {})
	server := object.get(tool, "serverName", "")
	not has_non_empty_text(hashes, [server])
	msg := sprintf("CRITICAL [Ch.8 MCP09]: unpinned MCP server %v missing from mcpSchemaHashes", [object.get(tool, "serverName", "<unnamed>")])
}

# Ch.8: refuse MCP entries with missing or malformed runtime/pinned SHA-256 hex hashes.
deny contains msg if {
	some tool in input.runtimeAgentConfig.mcpTools
	not has_non_empty_text(tool, ["currentSchemaHash"])
	msg := sprintf("CRITICAL [Ch.8 MCP]: missing currentSchemaHash for MCP server %v", [object.get(tool, "serverName", "<unnamed>")])
}

deny contains msg if {
	some tool in input.runtimeAgentConfig.mcpTools
	hashes := object.get(input, ["cryptographicProvenance", "mcpSchemaHashes"], {})
	server := object.get(tool, "serverName", "")
	pinned := object.get(hashes, [server], "")
	is_string(pinned)
	count(trim_space(pinned)) > 0
	not is_sha256_hex(pinned)
	msg := sprintf("CRITICAL [Ch.8 MCP]: pinned mcpSchemaHashes[%v] is not a valid 64-hex SHA-256 hash", [server])
}

deny contains msg if {
	some tool in input.runtimeAgentConfig.mcpTools
	current := object.get(tool, "currentSchemaHash", "")
	is_string(current)
	count(trim_space(current)) > 0
	not is_sha256_hex(current)
	msg := sprintf("CRITICAL [Ch.8 MCP]: currentSchemaHash for server %v is not a valid 64-hex SHA-256 hash", [object.get(tool, "serverName", "<unnamed>")])
}

# Ch.8: MCP schema rug-pull — runtime hash must match pinned baseline.
deny contains msg if {
	some tool in input.runtimeAgentConfig.mcpTools
	pinned := input.cryptographicProvenance.mcpSchemaHashes[tool.serverName]
	is_sha256_hex(pinned)
	is_sha256_hex(tool.currentSchemaHash)
	tool.currentSchemaHash != pinned
	msg := sprintf("CRITICAL [Ch.8 MCP]: schema hash drift for server %v", [tool.serverName])
}

# Ch.8: agentic scope requires explicit killSwitchEnabled=true and scopedCredentialsRequired=true.
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

# Ch.7/16: cross-model KV reuse without an alignment/isolation control (fail closed if omitted).
deny contains msg if {
	input.inferenceConfig.crossModelKvCacheReuse == true
	not input.inferenceConfig.kvAlignmentControlActive == true
	not input.inferenceConfig.tenantKvPartitioned == true
	msg := "HIGH [Ch.7/16]: cross-model KV cache reuse requires alignment control or tenant partition evidence"
}
