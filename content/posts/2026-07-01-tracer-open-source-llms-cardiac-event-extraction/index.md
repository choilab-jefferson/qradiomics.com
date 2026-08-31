---
title: "TRACER: Open-Source LLM Prompting Matches Specialized Medical AI for Cardiac Event Extraction"
date: "2026-07-01T09:00:00.000-04:00"
categories:
  - "news"
  - "research"
  - "ai"
tags:
  - "LLM"
  - "Prompt Engineering"
  - "EHR"
  - "NLP"
  - "Cardio-Oncology"
  - "GPT-OSS"
  - "DeepSeek"
  - "Llama"
  - "Mistral"
  - "Open Source"
aliases:
  - /2026/07/01/tracer-open-source-llms-cardiac-event-extraction/
  - /2026/07/27/tracer-open-source-llms-cardiac-event-extraction/
description: "TRACER shows that prompt-engineering rigor, not proprietary model weights, is what lets open-source LLMs extract cardiac events from unstructured EHRs. Now published in IJROBP (the Red Journal)."
cover:
  image: "images/tracer-ijrobp-pre-proof.jpg"
  alt: "IJROBP journal pre-proof page for the TRACER cardiac event extraction paper"
  relative: true
---

**The moat isn't the model. It's how you ask the question.**

I'm excited to share new work from our AI research team at the Sidney Kimmel Comprehensive Cancer Center (SKCC) at Jefferson: **TRACER**, a prompting framework that shows smart prompt engineering with open-source LLMs can solve one of the hardest problems in clinical research: extracting cardiac events from thousands of unstructured EHRs. The paper is now in press at *International Journal of Radiation Oncology, Biology, Physics* (IJROBP, the Red Journal).

## The problem

We worked with a cohort of **411 lung and breast cancer patients** across two institutions: a Jefferson development/internal-validation cohort (n=266) and an external validation cohort from Lehigh Valley Health Network (n=145). Cardiac events were physician-adjudicated from the full EHR history. Manual chart review at this scale is a major bottleneck for cardio-oncology research, and specialized medical AI models have historically plateaued well short of the accuracy needed to trust the output at scale.

## The TRACER framework

- **Two-phase pipeline**: fast structured queries first, followed by an open-source LLM with context-window filtering for the cases that need deeper reading.
- **Few-shot hard negatives**: examples that teach the model to correctly rule out a cardiac event (e.g., recognizing that "ruling out an MI" is not itself an MI).
- **Temporal awareness**: prompts explicitly distinguish pre-treatment from post-treatment context.
- **Fully local**: no proprietary APIs, no external dependencies, so it can run inside an institution's own infrastructure.

## Results

| | |
|---|---|
| **Accuracy** | 79–85% across development, internal, and external validation cohorts (best models: GPT-OSS, DeepSeek-R1, Llama-3.3, Mistral-Large) |
| **Processing time** | 20–42 sec/patient · 2.3–4.8 hours total for all 411 patients, vs. ~822 hours estimated for full manual chart review |
| **Fine-tuning required** | None |
| **Institutions** | Sidney Kimmel Comprehensive Cancer Center at Jefferson + Lehigh Valley Health Network |
| **Cohort** | 411 patients (development, internal-validation, and external-validation cohorts) |

**Interesting finding:** for this kind of straightforward event extraction, larger general-purpose open-source models actually outperformed medical domain-specific models, further evidence that careful prompting matters more than domain fine-tuning here.

## Why it matters

Clinical research is drowning in unstructured data, and most centers lack the infrastructure, or budget, for proprietary clinical AI platforms. TRACER shows that the bottleneck isn't model weights, it's prompt-engineering rigor. That's a democratizing result: any center with an open-source LLM and a well-designed prompting pipeline can replicate this approach, at a fraction of the cost of specialized clinical AI.

No more summer breaks spent by medical students manually digging through EHR free text: TRACER frees that time up for more meaningful clinical research.

## The team

Huge congratulations to **Dr. Wenchao Cao**, who finished his Senior Physics Residency with us and joined the department as medical physics faculty on July 1, where he is continuing this work, and **Dr. Nilanjan Haldar**, who just completed his Radiation Oncology residency and is heading to Phoenix. Much of the extraction and validation work was done by the student intern team: Isis Lloyd, Michael Dichmann, Moorin Khan, and Patrick Faherty, along with undergraduate Femi Adejolu. Best of luck to Wenchao and Nilanjan on their next chapters.

## Publication

**Cross-Institutional Validation of a Novel LLM-Based Cardiac Event Extraction Framework from Electronic Health Records.**
Wenchao Cao, Isis Lloyd, Michael Dichmann, Nilanjan Haldar, David Thomas, Zhe Chen, Erik Blomain, Femi Adejolu, Kristen E. Beck, Patrick Faherty, Moorin Khan, Nicole Simone, Varsha Jain, Eugene Storozynsky, Adam P. Dicker, **Wookjin Choi**, Yevgeniy Vinogradskiy.
*International Journal of Radiation Oncology, Biology, Physics* (in press), published online June 29, 2026.

- DOI: [10.1016/j.ijrobp.2026.06.3060](https://doi.org/10.1016/j.ijrobp.2026.06.3060)
- Full text: [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0360301626039131) · [Red Journal](https://www.redjournal.org/article/S0360-3016(26)03913-1/fulltext)

Sidney Kimmel Comprehensive Cancer Center at Jefferson, Sidney Kimmel Medical College, Thomas Jefferson University, with Lehigh Valley Health Network.

## Media coverage

- [Large Language Model-Based System Identifies Cardiac Event Data in Cancer Patients' Electronic Health Records (*Jefferson Investigates*, August 2026)](https://www.jefferson.edu/news/2026/08/aug-2026-roundup.html) ([our writeup](/posts/2026-08-31-jefferson-investigates-features-tracer/))

Thanks to everyone who worked on this. Excited to see other centers pick this approach up and put it to use.
