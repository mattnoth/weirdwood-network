# Model Selection Strategy

**Budget context:** $100/month = $25/week

This is a guidance document, not a hard rule. When delegating work or planning extraction passes, agents should be *conscious* of model choice and flag when cost efficiency might suggest an alternative. Matt decides based on quality/consistency tradeoffs.

## Task-by-Task Recommendations

| Task | Recommendation | Reasoning | Approx. Cost |
|------|---|---|---|
| **Pass 1: Mechanical Extraction** | Opus (consistency first) | Deterministic schema extraction; all books should use same model ≥1 time for quality parity. Future passes can optimize cost. | ~$200/book (1.1M input tokens @ Opus) |
| **Quote extraction** (for voice analysis prep) | Haiku | Pure pattern extraction: find dialogue tags and speaker lines. No reasoning needed. | ~$1.80 (344 chapters) |
| **Pass 3: Voice analysis** | Sonnet | Mid-tier reasoning: analyze speech patterns, audience effects, emotional register. Cheaper than Opus, sufficient for pattern work. | ~$150-200 total (50 POV characters) |
| **Pass 4: Foreshadowing scan** | Sonnet | Cross-reference chapters against known event list; reasoning needed but not deep synthesis. | ~$80-100 (344 chapters × Sonnet) |
| **Cross-character perception edges** | Sonnet or Python | If using LLM: Sonnet for spot-checks. Better: Python + data you already have. | <$50 (spot-checks only) |
| **Pass 5+: Open-ended discovery** | Opus | Novel pattern synthesis requires full reasoning depth. Use sparingly. | TBD |

## Cost Modeling

**Opus:**
- Input: $15/1M tokens (~$0.000015 per token)
- Output: $75/1M tokens (~$0.000075 per token)
- Use for: novel reasoning, final synthesis, quality validation

**Sonnet:**
- Input: $3/1M tokens (~$0.000003 per token)
- Output: $15/1M tokens (~$0.000015 per token)
- Use for: analysis, pattern extraction, reasoning on known structures

**Haiku:**
- Input: $0.80/1M tokens (~$0.0000008 per token)
- Output: $4/1M tokens (~$0.000004 per token)
- Use for: deterministic pattern matching, pre-processing, cheap validation

## Decision Questions for Agents

Before proposing work, consider:

1. **Is this deterministic or reasoning-heavy?**
   - Deterministic (find patterns, extract known fields) → Haiku/Sonnet
   - Reasoning (synthesize novel patterns, make judgment calls) → Sonnet/Opus

2. **Does consistency matter?**
   - All books need same quality baseline → stick with Opus for Pass 1, document it
   - Cost optimization on later passes → can switch models if validated

3. **Can Python do most of it?**
   - If yes, Python first, then LLM for edge cases only → saves 90% cost

4. **How much re-reading is involved?**
   - If the model has to traverse every line → expensive. Pre-process to reduce input.
   - If pre-processed (quotes extracted, summaries provided) → cheap.

## Session Tracking

All work sessions record the model(s) used in frontmatter:
```yaml
model: opus
```
or for mixed sessions:
```yaml
model: opus, sonnet
```

This enables auditing quality/cost correlation over time.
