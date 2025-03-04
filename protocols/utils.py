import re
import json


class SecurityUtils:
    @staticmethod
    def sanitize_output(text: str) -> str:
        """Remove sensitive patterns from output"""
        patterns = [
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
            r"\b(?:\d[ -]*?){13,16}\b"  # Credit cards
        ]
        for pattern in patterns:
            text = re.sub(pattern, "[REDACTED]", text)
        return text


class SafeJSONParser:
    @staticmethod
    def safe_parse(text: str) -> dict:
        """Robust JSON parsing with security checks"""
        try:
            sanitized = SecurityUtils.sanitize_output(text)
            return json.loads(sanitized)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON", "original": text}
