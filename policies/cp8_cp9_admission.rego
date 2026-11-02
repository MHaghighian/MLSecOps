# MLSecOps reference admission policy: bind CP8 release approval to CP9 deploy integrity.
# Input: Evidence Pack JSON (see schemas/evidence-pack.schema.json).
package mlsecops.admission

import rego.v1

default allow := false

allow if {
	count(deny) == 0
}

# CP8 → CP9 TOCTOU: digest approved at release must match artifact presented at deploy.
deny contains msg if {
	approved := input.lifecycleControlGates.cp8_releaseDecisionGate.boundToCp9Digest
	deployed := input.modelArtifact.sha256Digest
	approved != deployed
	msg := sprintf("CRITICAL [CP8->CP9]: model digest %v does not match CP8-approved digest %v", [deployed, approved])
}

deny contains msg if {
	input.lifecycleControlGates.cp8_releaseDecisionGate.decision != "APPROVED"
	msg := "CRITICAL [CP8]: release decision is not APPROVED"
}

deny contains msg if {
	input.cryptographicProvenance.cp9_checkpointVerified != true
	msg := "CRITICAL [CP9]: integrity/provenance checkpoint not verified"
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

# Ch.8: MCP schema rug-pull — runtime hash must match pinned baseline.
deny contains msg if {
	some tool in input.runtimeAgentConfig.mcpTools
	pinned := input.cryptographicProvenance.mcpSchemaHashes[tool.serverName]
	tool.currentSchemaHash != pinned
	msg := sprintf("CRITICAL [Ch.8 MCP]: schema hash drift for server %v", [tool.serverName])
}

# Ch.8: agentic scope requires kill-switch evidence.
deny contains msg if {
	input.metadata.systemScope == "Agentic-MCP"
	input.runtimeAgentConfig.killSwitchEnabled != true
	msg := "HIGH [Ch.8]: Agentic-MCP deploy requires killSwitchEnabled=true"
}

# Ch.7/16: cross-model KV reuse without an alignment/isolation control.
deny contains msg if {
	input.inferenceConfig.crossModelKvCacheReuse == true
	input.inferenceConfig.kvAlignmentControlActive != true
	input.inferenceConfig.tenantKvPartitioned != true
	msg := "HIGH [Ch.7/16]: cross-model KV cache reuse requires alignment control or tenant partition evidence"
}
