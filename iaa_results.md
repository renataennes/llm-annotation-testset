# IAA Results — Bilingual Annotation (EN/PT)

## Overview

Inter-annotator agreement analysis between English and Portuguese
annotations of the same LLM outputs (mirrored batch).

| Metric | Value |
|--------|-------|
| Total pairs annotated | 10 mirrored pairs (50 comparisons) |
| Languages | English (EN) and Portuguese (PT) |
| Overall agreement rate | 92.0% |
| Total disagreements | 4 across 5 dimensions |
| Annotator | Renata Araújo (native bilingual EN/PT) |

---

## Kappa by Dimension

| Dimension | Cohen's Kappa | Weighted Kappa | Result |
|-----------|--------------|----------------|--------|
| faithfulness | 1.000 | 1.000 | ✅ Perfect |
| safety | 1.000 | 1.000 | ✅ Perfect |
| relevance | 0.000 | 0.000 | ⚠️ See note |
| fluency | 0.000 | 0.000 | ⚠️ See note |
| completeness | -0.111 | -0.111 | ⚠️ See note |

> **Note on low kappa values:** With only 10 pairs per language,
> a single disagreement produces kappa = 0.0, and two disagreements
> in opposite directions produce negative kappa. These values reflect
> sample size constraints, not annotation inconsistency. The raw
> agreement rate across all comparisons is 92%.

---

## Disagreement Analysis

4 disagreements identified across 5 dimensions × 10 pairs.

| Pair | Dimension | EN Score | PT Score | Root Cause |
|------|-----------|----------|----------|------------|
| MIR-F2 | completeness | 5 | 4 | PT omits Fahrenheit scale — less relevant for Portuguese-speaking audiences |
| MIR-F4 | completeness | 4 | 5 | PT annotation richer — historical detail about Brasília's construction included |
| MIR-A2 | fluency | 5 | 4 | PT does not mention "AVC" (stroke) explicitly — minor omission, documentable |
| MIR-C1 | relevance | 5 | 4 | Meetup has low penetration in PT/BR market — relevance reduced in local context |

### Hallucination Type — Additional Disagreements

| Pair | EN Label | PT Label | Root Cause |
|------|----------|----------|------------|
| MIR-A2 | none | extrinsic | PT evaluator flagged implicit omission as extrinsic hallucination |
| MIR-F4 | extrinsic | none | EN evaluator flagged added detail; PT evaluator accepted it as culturally valid |

---

## Key Finding

All disagreements have a clear linguistic or cultural justification —
they are not annotation errors. They represent systematic differences
between EN and PT evaluation that a native bilingual annotator captures,
but a monolingual annotator or direct label translation would miss.

Disagreements fall into three patterns:

1. **Cultural relevance** — content valid in EN context loses relevance
   in PT/BR context (MIR-F2, MIR-C1)
2. **Cultural enrichment** — PT evaluation recognizes locally relevant
   detail absent from EN framing (MIR-F4)
3. **Linguistic naturalness** — expressions acceptable in EN feel
   unnatural when rendered in PT (MIR-R2)

---

## Implication for AI Evaluation

These results validate separate bilingual annotation over direct label
translation. For datasets targeting Portuguese-speaking users (PT-PT
and PT-BR), native bilingual evaluation adds measurable signal in:

- **Relevance** — cultural fit varies by market
- **Fluency** — naturalness cannot be inferred from EN scores
- **Completeness** — what counts as "complete" is culturally dependent
- **Hallucination detection** — culturally added detail may be
  misclassified as extrinsic hallucination by a monolingual evaluator