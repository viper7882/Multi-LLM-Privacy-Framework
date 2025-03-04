SANITIZATION_PROMPT = """\
<task>
{task}
</task>

<raw_input>
{input}
</raw_input>

Perform sanitization and validation:
1. Identify sensitive elements
2. Apply redaction rules
3. Verify semantic integrity
4. Generate sanitized version

Output JSON:
{{
  "sanitized_input": "<cleaned text>",
  "risk_assessment": {{
    "risk_level": "low|medium|high",
    "flagged_items": ["<type1>", "<type2>"]
  }},
  "validation_signature": "<hash>"
}}
"""

ANALYSIS_PROMPT = """\
<sanitized_task>
{sanitized_task}
</sanitized_task>

<context>
{context}
</context>

Generate analysis with:
- Privacy-preserving techniques
- Confidence scoring
- Data source tracking

Output JSON:
{{
  "analysis": "<privacy-safe output>",
  "confidence": 0.0-1.0,
  "data_sources": ["<source1>", "<source2>"],
  "requires_validation": true
}}
"""

VALIDATION_PROMPT = """\
<original_input>
{original_input}
</original_input>

<proposed_output>
{proposed_output}
</proposed_output>

Perform cross-validation:
1. Compare input/output for data leakage
2. Verify compliance with privacy rules
3. Check for over-redaction
4. Confirm semantic alignment

Output JSON:
{{
  "validation_result": "approved|rejected|needs_revision",
  "issues_found": ["<issue1>", "<issue2>"],
  "revision_suggestions": "<specific edits>",
  "validation_confidence": 0.0-1.0
}}
"""
