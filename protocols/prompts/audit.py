AUDIT_PROMPT = """\
<conversation_history>
{history}
</conversation_history>

<system_logs>
{logs}
</system_logs>

Generate privacy audit report:
1. Identify potential compliance issues
2. Flag suspicious patterns
3. Suggest improvements
4. Maintain chain of custody

Output JSON:
{{
  "audit_summary": "<overview>",
  "critical_issues": [
    {{
      "type": "<issue_type>",
      "severity": "low|medium|high",
      "location": "<log_ref>",
      "recommendation": "<action>"
    }}
  ],
  "compliance_score": 0-100
}}
"""
