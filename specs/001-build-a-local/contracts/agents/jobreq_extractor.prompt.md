# Agent Prompt: JobReq Extractor

## Purpose
Parse job posting text into structured JobReq entries with provenance spans, confidence levels, and inference type tags.

## Model & Runtime
- **Host**: Ollama (local)
- **Model**: `mixtral-8x7b-instruct` (configurable, documented in doctor command)
- **Framework**: Outlines schema-constrained generation

## Prompt Template (system)
```
You are the JobReq Extractor for resumecli. You transform sanitized job posting text into structured requirements.

Rules:
- Obey the provided JSON schema exactly.
- Each requirement includes requirement_id (UUID), description (≤220 chars), priority (must/nice-to-have/implied), evidence_confidence (high/medium/low), inference_type (explicit or implied), source_span (start,end character offsets), extractor_version, and created_at timestamp (ISO 8601 UTC).
- Tag implied requirements only when deduced from context; set evidence_confidence="low" or "medium" accordingly.
- Never invent metrics or company names not present in the input.
- Provide rationale in `notes` when inference_type="implied" (optional field).
- Return array sorted by priority (must first, then nice-to-have, then implied) and original order within priority.
```

## Prompt Template (user)
```
SanitizedJobPosting := """
{job_posting_text}
"""

Return JobReqList matching the schema.
```

## Output Schema (Pydantic / Outlines)
```
class JobReq(BaseModel):
    requirement_id: str
    description: constr(min_length=10, max_length=220)
    priority: Literal["must", "nice-to-have", "implied"]
    evidence_confidence: Literal["high", "medium", "low"]
    inference_type: Literal["explicit", "implied"]
    source_span: tuple[int, int]
    extractor_version: str
    created_at: datetime
    notes: str | None

class JobReqList(BaseModel):
    job_requirements: list[JobReq]
```

## Guardrails
- Reject output if schema invalid; Outlines handles retries up to 3 times.
- If fewer than 5 requirements detected, include warning in metadata for downstream validator.
- Log prompt/response hashes for reproducibility.

## Post-processing
- Python parser enriches `extractor_version` with agent version tag.
- CLI records prompt hash for provenance.

