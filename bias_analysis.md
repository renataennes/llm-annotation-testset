# LLM-as-a-Judge Bias Analysis

## Overview

Empirical analysis of systematic biases in LLM-based automatic evaluation.
Three experiments were designed to test whether the judge's verdicts are
influenced by factors unrelated to response quality.

| Setting | Value |
|---------|-------|
| Dataset | annotations_mirrored_batch.csv (10 EN/PT pairs) |
| Judge model | llama-3.1-8b-instant (Groq) |
| Total verdicts collected | 30 (10 per experiment) |
| Temperature | 0 (deterministic) |

---

## Results Summary

| Experiment | Bias Rate | Level |
|------------|-----------|-------|
| Position Bias | 0% | 🟢 Low |
| Verbosity Bias | 30% | 🟡 Moderate |
| Confidence Bias | 100% | 🔴 High |

---

## Experiment 1 — Position Bias

**Question:** Does the judge change its verdict when response order is swapped?

**Method:** Each pair was sent twice — original order (EN=A, PT=B)
then reversed (PT=A, EN=B). Verdicts were normalized for comparison.

**Result:** 0 out of 10 pairs changed verdict on reversal.

**Conclusion:** The judge shows no position bias on this dataset.
Verdicts are stable regardless of which response appears first —
a positive reliability signal for this model at temperature=0.

---

## Experiment 2 — Verbosity Bias

**Question:** Does the judge prefer longer responses regardless of quality?

**Method:** Response length (word count) was compared against the
judge's verdict. Bias was flagged when the longer response won.

**Result:** 3 out of 10 pairs showed verbosity bias (30%).

**Conclusion:** Moderate verbosity bias detected. In 3 cases the judge
favored the longer response. This is consistent with findings in
LLM evaluation literature — length can act as a proxy for perceived
thoroughness, even when it does not reflect actual quality.

---

## Experiment 3 — Confidence Bias

**Question:** Does confident tone inflate the judge's score?

**Method:** Each EN response was duplicated into two versions with
identical content but different openings:
- Version A: "I'm certain that: [response]"
- Version B: "I think, but I'm not sure: [response]"

**Result:** 10 out of 10 pairs favored the confident version (100%).

**Conclusion:** Confidence bias is systematic and severe in this model.
The judge consistently preferred responses framed with certainty,
regardless of content. This is a critical finding for any pipeline
using this model as an automatic evaluator — tone alone can override
quality in the verdict.

---

## Overall Takeaway

| Bias Type | Risk for Production Pipelines |
|-----------|-------------------------------|
| Position | ✅ Low risk — verdicts are stable |
| Verbosity | ⚠️ Moderate — penalizes concise but accurate responses |
| Confidence | 🚨 High risk — tone overrides content systematically |

These results suggest that llama-3.1-8b-instant is reliable for
position-invariant evaluation but should **not** be used without
human oversight in tasks where response tone varies — such as
medical, legal, or safety-critical content where hedged language
is appropriate and expected.

---

## Files

| File | Contents |
|------|----------|
| `data/inter_annotator/bias_position.csv` | Raw results — Experiment 1 |
| `data/inter_annotator/bias_verbosity.csv` | Raw results — Experiment 2 |
| `data/inter_annotator/bias_confidence.csv` | Raw results — Experiment 3 |
| `notebooks/04_bias_analysis.ipynb` | Full reproducible code |