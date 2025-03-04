FALLBACK_PROMPT = """\
<error_type>
{error_type}
</error_type>

<error_context>
{context}
</error_context>

Generate safe error response:
- Acknowledge error generically
- Never expose system details
- Suggest alternative phrasing
- Maintain professional tone

Output JSON:
{{
  "user_message": "<safe error message>",
  "internal_code": "E{code}",
  "retry_suggestion": "<generic advice>"
}}
"""
