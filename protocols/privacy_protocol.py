import hashlib
import json

from typing import Optional, List, Dict
from dataclasses import dataclass, field

from .clients import OllamaClient, OpenAIClient
from protocols.utils import SafeJSONParser
from protocols.prompts import core, interaction

from dataclasses import dataclass, field
from typing import Optional, Dict, List


@dataclass
class PrivacyDecision_v2:
    """Enhanced decision class with cryptographic validation and compliance tracking"""

    # Core response data
    content: Optional[Dict] = None
    error: Optional[str] = None

    # Processing metadata
    requires_additional_processing: bool = False
    confidence_score: float = 0.0

    # Data provenance
    data_sources: List[str] = field(default_factory=list)
    input_digest: Optional[str] = None
    processing_signature: Optional[str] = None

    # Compliance tracking
    compliance_status: Dict = field(default_factory=lambda: {
        "gdpr": {
            "article32": False,
            "recital75": False
        },
        "hipaa": {
            "safe_harbor": False,
            "expert_determination": False
        }
    })

    # Privacy metrics
    privacy_controls: Dict = field(default_factory=lambda: {
        "applied_techniques": [],
        "residual_risk": "low/medium/high"
    })

    # Audit trail
    audit_records: Dict = field(default_factory=lambda: {
        "processing_steps": [],
        "risk_mitigations": [],
        "validation_checksum": None
    })

    def is_compliant(self) -> bool:
        """Check if decision meets all compliance requirements"""
        return all(
            self.compliance_status["gdpr"].values()
        ) and all(
            self.compliance_status["hipaa"].values()
        )

    def validate_integrity(self) -> bool:
        """Verify cryptographic data integrity"""
        if not self.input_digest or not self.content:
            return False
        generated_hash = hashlib.sha256(
            json.dumps(self.content).encode()
        ).hexdigest()
        return generated_hash == self.input_digest.split(":")[-1]

    def to_dict(self) -> Dict:
        """Convert to dictionary with all metadata"""
        return {
            "content": self.content,
            "error": self.error,
            "processing_metadata": {
                "requires_additional_processing": self.requires_additional_processing,
                "confidence_score": self.confidence_score
            },
            "provenance": {
                "data_sources": self.data_sources,
                "input_digest": self.input_digest,
                "processing_signature": self.processing_signature
            },
            "compliance_status": self.compliance_status,
            "privacy_controls": self.privacy_controls,
            "audit_records": self.audit_records
        }


class PrivacyProtocol_v2:
    def __init__(self, local_llm, remote_llm, doc_metadata: str, data_types: List[str], max_rounds: int = 3):
        self.local_llm = local_llm
        self.remote_llm = remote_llm
        self.doc_metadata = doc_metadata
        self.data_types = data_types
        self.max_rounds = max_rounds
        self.parser = SafeJSONParser()

    def analyze_response(self, response: str) -> PrivacyDecision_v2:
        """Enhanced analysis with cryptographic validation"""
        try:
            parsed = self.parser.safe_parse(response)

            # Validate cryptographic hashes
            input_hash = parsed.get("provenance_verification", {}).get("input_digest", "")
            if not self._validate_hash(parsed["data"], input_hash):
                raise ValueError("Data hash mismatch")

            return PrivacyDecision_v2(
                content=parsed.get("data", {}).get("content"),
                confidence_score=parsed.get("compliance_metadata", {}).get("confidence_score", 0.0),
                data_sources=parsed.get("provenance_verification", {}).get("data_sources", []),
                compliance_status=parsed.get("compliance_metadata", {})
            )
        except json.JSONDecodeError as e:
            return PrivacyDecision_v2(error=f"Invalid JSON: {str(e)}")

    def process_query(self, task: str, context: List[str], risk_threshold: str = "medium") -> Dict:
        """Enhanced multi-stage processing with audit trail"""
        # Generate cryptographic context hash
        context_str = "\n\n".join(context)
        context_hash = hashlib.sha256(context_str.encode()).hexdigest()

        # Initialize privacy-preserving worker
        worker_prompt = core.WORKER_SYSTEM_PROMPT.format(
            doc_metadata=self.doc_metadata,
            context_hash=context_hash,
            data_types=self.data_types
        )
        self.local_llm.set_system_prompt(worker_prompt)

        # Initialize processing state
        current_round = 0
        final_output = None
        processing_history = []
        requires_processing = True

        while requires_processing and current_round < self.max_rounds:
            current_round += 1

            # Supervisor Initial Directive
            supervisor_initial = core.SUPERVISOR_INITIAL_PROMPT.format(
                task=task,
                doc_metadata=self.doc_metadata,
                context_hash=context_hash,
                risk_threshold=risk_threshold,
                current_round=current_round
            )
            directive = self.remote_llm.generate(supervisor_initial)

            # Worker Processing
            worker_response = self.local_llm.generate(
                f"Round {current_round} Directive: {directive}\nContext: {context_str}"
            )

            # Supervisor Validation
            supervisor_convo = core.SUPERVISOR_CONVERSATION_PROMPT.format(
                response=worker_response,
                context_hash=context_hash,
                remaining_rounds=self.max_rounds - current_round
            )
            validation = self.remote_llm.generate(supervisor_convo)

            # Parse decision
            decision = self.analyze_response(validation)
            processing_history.append({
                "round": current_round,
                "directive": directive,
                "worker_response": worker_response,
                "validation": validation,
                "decision": decision
            })

            # Check termination conditions
            if decision.decision_type == "finalize" or current_round >= self.max_rounds:
                requires_processing = False
                final_output = self._finalize_output(
                    validation,
                    current_round,
                    context_hash
                )
                break

        return {
            "final_output": final_output,
            "processing_rounds": current_round,
            "processing_history": processing_history,
            "audit_trail": self._create_audit_trail(context_hash, current_round),
            "termination_reason": "max_rounds" if current_round >= self.max_rounds else "final_decision"
        }

    def _finalize_output(self, validation: str, rounds: int, context_hash: str) -> Dict:
        """Handle final output generation"""
        supervisor_final = core.SUPERVISOR_FINAL_PROMPT.format(
            response=validation,
            query_count=rounds,
            mitigation_count=len(self.data_types),
            response_hash=hashlib.sha256(validation.encode()).hexdigest()
        )
        return json.loads(self.remote_llm.generate(supervisor_final))

    def _create_audit_trail(self, context_hash: str, rounds: int) -> Dict:
        """Generate comprehensive audit trail"""
        return {
            "context_hash": context_hash,
            "total_rounds": rounds,
            "privacy_operations": self.local_llm.privacy_metrics,
            "compliance_checks": self.remote_llm.compliance_metrics,
            "final_validation": hashlib.sha256(
                json.dumps(self.local_llm.usage_stats).encode()
            ).hexdigest()
        }

    def _validate_hash(self, data: str, stored_hash: str) -> bool:
        """Verify cryptographic data integrity"""
        generated_hash = hashlib.sha256(data.encode()).hexdigest()
        return generated_hash == stored_hash.split(":")[-1]

    def _compile_usage(self) -> dict:
        """Enhanced usage statistics with privacy metrics"""
        return {
            "local": {
                **self.local_llm.usage_stats,
                "privacy_ops": self.local_llm.privacy_metrics
            },
            "remote": {
                **self.remote_llm.usage_stats,
                "compliance_checks": self.remote_llm.compliance_metrics
            }
        }


class PrivacyProtocol_v1:
    """Core privacy protocol implementation"""

    def __init__(
            self,
            local_llm: OllamaClient,
            remote_llm: OpenAIClient,
            sensitivity_threshold: float = 0.7
    ):
        self.local_llm = local_llm
        self.remote_llm = remote_llm
        self.sensitivity_threshold = sensitivity_threshold

    def detect_sensitive_data(self, text: str) -> bool:
        """Determine if input contains sensitive data (placeholder implementation)"""
        # In practice, implement with regex/NLP model/classification
        sensitive_keywords = ["ssn", "credit card", "medical", "password"]
        return any(keyword in text.lower() for keyword in sensitive_keywords)

    def process_query(self, prompt: str) -> str:
        """Route queries based on sensitivity detection"""
        if self.detect_sensitive_data(prompt):
            return self.local_llm.generate(prompt)
        else:
            return self.remote_llm.generate(prompt)

    def hybrid_generation(self, prompt: str) -> str:
        """Combine both LLMs for enhanced accuracy"""
        # Local LLM processes sensitive parts
        sanitized_prompt = self.local_llm.generate(f"Sanitize this input: {prompt}")
        # Remote LLM handles complex processing
        return self.remote_llm.generate(f"Process this sanitized input: {sanitized_prompt}")
