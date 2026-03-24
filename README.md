# 📝 LLM Annotation Testset — Bilingual EN/PT

Bilingual annotation dataset and quality analysis for LLM output evaluation.
Annotated by a native EN/PT evaluator across 5 quality dimensions.

**Stack:** Python · Pandas · Scikit-learn · HuggingFace Datasets · Groq API  
**Status:** ✅ Complete — 106 pairs annotated

**Published on:** [HuggingFace Datasets →](https://huggingface.co/datasets/renataennes/llm-eval-bilingual)

---

## 📊 Results at a Glance

| Metric | Value |
|--------|-------|
| Total pairs annotated | 106 |
| Languages | English (EN) + Portuguese (PT) |
| Mirrored pairs (EN/PT) | 10 |
| Overall agreement rate | 92.0% |
| Cohen's Kappa — faithfulness | 1.000 ✅ |
| Cohen's Kappa — safety | 1.000 ✅ |
| Disagreements documented | 4 |
| Bias experiments conducted | 3 |
| Confidence bias detected | 🔴 100% |
| Position bias detected | 🟢 0% |

---

## 📌 Overview

A curated, human-annotated test set of **106 LLM response pairs** in English
and Portuguese, designed to benchmark language model quality across
faithfulness, relevance, fluency, completeness, and safety.

This dataset was built from scratch following professional annotation
guidelines used at companies like Scale AI, Anthropic, and DataAnnotation —
including adversarial prompts, ambiguous queries, and hard negatives.

---

## 🎯 Objectives

- Design and document a professional annotation rubric from scratch
- Collect diverse prompt types (factual, reasoning, adversarial, ambiguous)
- Annotate 100 LLM responses with multi-dimensional quality labels
- Ensure bilingual coverage (EN + PT) with equivalent difficulty
- Validate annotation quality with Cohen's Kappa and bilingual calibration
- Empirically measure LLM-as-a-Judge biases with 3 controlled experiments

---

## 🗂️ Project Structure
```
llm-annotation-testset/
│
├── data/
│   ├── raw/                          # Original prompts and responses
│   ├── annotated/
│   │   ├── annotations_EN_batch1.csv
│   │   ├── annotations_PT_batch1.csv
│   │   ├── annotations_mirrored_batch.csv
│   │   └── annotations_edge_cases.csv
│   └── inter_annotator/
│       ├── kappa_report.csv
│       ├── bias_position.csv
│       ├── bias_verbosity.csv
│       └── bias_confidence.csv
│
├── notebooks/
│   ├── 03_cohen_kappa_IAA.ipynb      # Inter-annotator agreement
│   └── 04_bias_analysis.ipynb        # LLM-as-a-Judge bias experiments
│
├── iaa_results.md                    # Bilingual calibration analysis
├── bias_analysis.md                  # LLM-as-a-Judge bias findings
├── ANNOTATION_RUBRIC.md              # Full annotation guidelines
├── requirements.txt
└── README.md
```

---

## 🧠 Annotation Rubric (Summary)

Full rubric in [`ANNOTATION_RUBRIC.md`](ANNOTATION_RUBRIC.md)

### Dimensions Annotated (each scored 1–5)

| Dimension | Description |
|-----------|-------------|
| **Faithfulness** | Is every claim grounded in verifiable facts or provided context? |
| **Relevance** | Does the response address what the user actually needed? |
| **Fluency** | Is the language natural, clear, and well-structured? |
| **Completeness** | Does the response cover all aspects of the question? |
| **Safety** | Does the response avoid harmful or dangerous content? |

---

## 🔍 Key Findings

### Bilingual Calibration

Agreement rate of **92%** across 50 comparisons (10 mirrored pairs × 5 dimensions).
All 4 disagreements have clear linguistic or cultural justification:

| Pair | Dimension | Root Cause |
|------|-----------|------------|
| MIR-F2 | Completeness | PT omits Fahrenheit — less relevant for Portuguese audiences |
| MIR-F4 | Completeness | PT richer — historical detail about Brasília included |
| MIR-A2 | Fluency | PT does not mention AVC explicitly — minor omission |
| MIR-C1 | Relevance | Meetup has low penetration in PT/BR market |

### LLM-as-a-Judge Bias (llama-3.1-8b-instant)

| Experiment | Bias Rate | Level |
|------------|-----------|-------|
| Position Bias | 0% | 🟢 Low |
| Verbosity Bias | 30% | 🟡 Moderate |
| Confidence Bias | 100% | 🔴 High |

> Confidence bias is systematic and severe — tone alone overrides content
> in automatic verdicts. Human oversight is essential in tasks where
> hedged language is appropriate (medical, legal, safety-critical content).

---

## 🔧 Tech Stack

| Tool | Role |
|------|------|
| `Python` | Annotation and analysis |
| `Pandas` | Dataset manipulation |
| `Scikit-learn` | Cohen's Kappa calculation |
| `Groq API` | LLM-as-a-Judge (llama-3.1-8b-instant) |
| `HuggingFace Datasets` | Publishing and versioning |

---

## 🚀 Getting Started
```bash
# 1. Clone
git clone https://github.com/renataennes/llm-annotation-testset
cd llm-annotation-testset

# 2. Install
pip install -r requirements.txt

# 3. Add your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# 4. Run inter-annotator agreement
jupyter notebook notebooks/03_cohen_kappa_IAA.ipynb

# 5. Run bias analysis
jupyter notebook notebooks/04_bias_analysis.ipynb
```

---


## 🔗 Related Projects

- [Project 1 — RAG Hallucination Detector](../project1-rag-hallucination/)
- [Project 3 — LLM Eval Dashboard](../project3-eval-dashboard/)

---

*Built as part of an AI Model Evaluation portfolio. Author: Renata Araújo — [LinkedIn](https://www.linkedin.com/in/renata-araujo-en/)*
