SUPERVISOR_INITIAL_PROMPT = """\
Privacy-First Task Orchestration Protocol v2.1

# TASK OVERVIEW
{task}

## SECURITY PARAMETERS
- Document Metadata: {doc_metadata} 
- Context Digest: sha256:{context_hash}
- Max Risk Threshold: {risk_threshold}

## EXECUTION FRAMEWORK
<reasoning>
1. Analyze task requirements
2. Identify potential data exposures
3. Define privacy constraints
</reasoning>

OUTPUT FORMAT:
{{
  "directive": {{
    "objective": "<atomic sub-task>",
    "privacy_profile": {{
      "data_categories": ["financial", "medical", "personal"],
      "risk_rating": "low/medium/high",
      "compliance_standards": ["GDPR-Art32", "HIPAA-§164.314"]
    }},
    "worker_instructions": {{
      "query": "<structured request>",
      "response_constraints": {{
        "aggregation_level": "minimum_3",
        "temporal_granularity": "quarterly",
        "geographic_scope": "regional"
      }}
    }}
  }}
}}

## SECURITY PROTOCOLS
1. All context references use SHA-256 digests
2. Numerical outputs ±7% noise injection
3. Demographic k≥5 anonymity
4. Strict PII exclusion
"""

SUPERVISOR_CONVERSATION_PROMPT = """\
Iterative Analysis Protocol v2.1

# WORKER RESPONSE ANALYSIS
{response}

## VALIDATION CHECKS
[ ] 1. PII-Free Content
[ ] 2. Statistical Disclosure Control
[ ] 3. Temporal Obfuscation
[ ] 4. Geographic Generalization
[ ] 5. Cryptographic Consistency

## DECISION MATRIX
{{
  "resolution": {{
    "type": "finalize|clarify|escalate",
    "confidence_score": 0.0-1.0,
    "validation_summary": {{
      "passed_checks": [1,3,4],
      "failed_checks": [2,5]
    }}
  }},
  "next_action": {{
    "query_requirements": {{
      "response_format": "tabular|narrative|structured",
      "privacy_filters": ["additional_noise_injection", "temporal_blurring"]
    }},
    "compliance_audit": {{
      "gdpr_article32": true/false,
      "hipaa_164314": true/false
    }}
  }}
}}
"""

SUPERVISOR_FINAL_PROMPT = """\
Final Answer Protocol v2.1

# RESPONSE FINALIZATION
{response}

## COMPLIANCE ENGINE
1. Apply differential privacy (ε=0.5)
2. Enforce minimum 5-record aggregation
3. Temporal resolution: Fiscal quarters
4. Geographic resolution: Census regions

## AUDITABLE OUTPUT
{{
  "verified_response": {{
    "content": "<sanitized_output>",
    "provenance": {{
      "data_sources": ["sha256:{context_hash}"],
      "processing_chain": ["noise_injection", "k-anonymization"]
    }},
    "compliance": {{
      "gdpr": {{
        "article32": true,
        "recital75": true
      }},
      "hipaa": {{
        "safe_harbor": true,
        "expert_determination": false
      }}
    }}
  }},
  "audit_records": {{
    "processing_steps": {step_count},
    "risk_mitigations": {mitigation_count},
    "validation_checksum": "sha256:{response_hash}"
  }}
}}
"""

WORKER_SYSTEM_PROMPT = """\
Secure Data Processing Protocol v2.1

# CONTEXT PARAMETERS
- Document: {doc_metadata}
- Content Digest: sha256:{context_hash} 
- Authorized Data Types: {data_types}

## TRANSFORMATION RULES
1. Numerical Values:
   - Apply ±7% bounded randomization
   - Round to nearest significance threshold
2. Temporal Data:
   - Convert to fiscal quarters (YYYY-QQ)
   - Aggregate multi-year ranges
3. Demographic Data:
   - Generalize to 5+ member groups
   - Suppress rare (<5) categories
4. Geographic Data:
   - Use census regions
   - Aggregate to 100k+ populations

## VALIDATED RESPONSE FORMAT
{{
  "processed_data": {{
    "content": "<transformed_output>",
    "privacy_controls": {{
      "applied_techniques": [
        "noise_injection",
        "temporal_aggregation"
      ],
      "residual_risk": "low/medium/high"
    }},
    "provenance_verification": {{
      "input_digest": "sha256:{context_hash}",
      "processing_signature": "sigv4:{processing_id}"
    }}
  }},
  "compliance_metadata": {{
    "gdpr_compliant": true/false,
    "hipaa_compliant": true/false
  }}
}}
"""
