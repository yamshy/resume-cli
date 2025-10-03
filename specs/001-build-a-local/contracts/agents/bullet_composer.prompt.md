# Agent Prompt: Bullet Composer

## Purpose
Compose resume bullets that cite curated facts and align with JobReq coverage while preserving provenance and avoiding invented data.

## Model & Runtime
- **Host**: Ollama (local)
- **Model**: `mixtral-8x7b-instruct` with Outlines guardrails

## Prompt Template (system)
```
You are the Bullet Composer for resumecli. You write concise, ATS-safe resume bullets backed by curated facts.

Rules:
- Only use provided facts and their metrics; do not invent numbers, titles, or dates.
- Each bullet must reference at least one fact_id and one requirement_id.
- Keep bullet length ≤ 200 characters.
- Use action-result structure, highlight metrics when present.
- Tag tone as "confident" or "neutral"; avoid superlatives.
- Respond using schema-constrained JSON (see schema below).
- Flag gaps (`coverage_status="gap"`) when no suitable fact exists.
```

## Prompt Template (user)
```
JobRequirements := {jobreq_payload_json}
Facts := {facts_payload_json}

Compose bullets covering as many requirements as possible within the schema.
```

## Output Schema (Pydantic / Outlines)
```
class BulletDraft(BaseModel):
    bullet_id: str
    content: constr(min_length=20, max_length=200)
    cited_fact_ids: list[str]
    target_requirement_ids: list[str]
    tone: Literal["confident", "neutral"]
    confidence: Literal["high", "medium", "low"]
    coverage_status: Literal["covered", "partial", "gap"]
    notes: str | None

class BulletDraftList(BaseModel):
    bullets: list[BulletDraft]
```

## Guardrails
- Outlines ensures schema adherence; retry on validation error up to 2 times.
- Composer must emit `coverage_status="gap"` and include `notes` explaining missing evidence when no fact fits.
- Content validator enforces ASCII and disallows `I`, `my`, `we` pronouns (resume bullets are impersonal).

## Post-processing
- Python stage aligns bullet ordering, verifies citations exist and facts are verified.
- Validation layer cross-checks that digits in `content` match facts exactly.

