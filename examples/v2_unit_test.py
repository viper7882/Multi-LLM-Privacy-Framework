import hashlib
import json

from protocols.prompts import core


# Medical context (sensitive data)
context = """
Patient John Doe is a 60-year-old male with a history of hypertension. In his latest checkup, his blood pressure was recorded at 160/100 mmHg, and he reported occasional chest discomfort during physical activity.
Recent laboratory results show that his LDL cholesterol level is elevated at 170 mg/dL, while his HDL remains within the normal range at 45 mg/dL. Other metabolic indicators, including fasting glucose and renal function, are unremarkable.
"""
task = "Evaluate cardiovascular risk based on BP and LDL readings"

# Generate context hash
context_hash = hashlib.sha256(context.encode()).hexdigest()

# Initialize Worker System Prompt
worker_prompt = core.WORKER_SYSTEM_PROMPT.format(
    doc_metadata="Patient Medical Record",
    context_hash=context_hash,
    data_types=["medical", "biometric"],
    processing_id="med_process_001",
)

# Supervisor Initial Prompt
supervisor_initial = core.SUPERVISOR_INITIAL_PROMPT.format(
    task=task,
    doc_metadata="Patient Medical Record",
    context_hash=context_hash,
    risk_threshold="high"
)

# Worker Response (simulated)
worker_response = {
    "processed_data": {
        "content": {
            "vital_analysis": {
                "blood_pressure": "Stage 2 Hypertension",
                "cholesterol_risk": "Elevated LDL (162-178 mg/dL)",
                "activity_symptoms": "Exercise-induced discomfort"
            }
        },
        "privacy_controls": {
            "applied_techniques": [
                "identifier_suppression",
                "numerical_noise_injection",
                "temporal_aggregation"
            ],
            "residual_risk": "low"
        },
        "provenance_verification": {
            "input_digest": f"sha256:{context_hash}",
            "processing_signature": "sigv4:med_process_001"
        }
    },
    "compliance_metadata": {
        "gdpr_compliant": True,
        "hipaa_compliant": True
    }
}

# Supervisor Conversation Prompt
supervisor_convo = core.SUPERVISOR_CONVERSATION_PROMPT.format(
    response=json.dumps(worker_response, indent=2)
)

# Supervisor Decision (simulated)
supervisor_decision = {
    "resolution": {
        "type": "clarify",
        "confidence_score": 0.85,
        "validation_summary": {
            "passed_checks": [1, 3, 4],
            "failed_checks": [2, 5]
        }
    },
    "next_action": {
        "query_requirements": {
            "response_format": "structured",
            "privacy_filters": ["additional_noise_injection"]
        },
        "compliance_audit": {
            "gdpr_article32": True,
            "hipaa_164314": True
        }
    }
}

# Final Worker Response
final_worker_response = {
    "processed_data": {
        "content": {
            "risk_assessment": "High cardiovascular risk profile",
            "recommendations": [
                "Immediate antihypertensive therapy",
                "LDL reduction target: <150 mg/dL",
                "Stress test evaluation"
            ]
        },
        "privacy_controls": {
            "applied_techniques": [
                "k-anonymization(k=5)",
                "numerical_bucketing"
            ],
            "residual_risk": "medium"
        },
        "provenance_verification": {
            "input_digest": f"sha256:{context_hash}",
            "processing_signature": "sigv4:med_process_002"
        }
    },
    "compliance_metadata": {
        "gdpr_compliant": True,
        "hipaa_compliant": True
    }
}

# Supervisor Final Prompt
supervisor_final = core.SUPERVISOR_FINAL_PROMPT.format(
    response=json.dumps(final_worker_response, indent=2),
    step_count=4,
    mitigation_count=3,
    response_hash=hashlib.sha256(
        json.dumps(final_worker_response).encode()
    ).hexdigest(),
    context_hash=context_hash,
)
