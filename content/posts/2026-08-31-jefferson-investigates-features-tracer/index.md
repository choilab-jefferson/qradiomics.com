---
title: "Jefferson Investigates features our TRACER cardiac event extraction study"
date: "2026-08-31T12:00:00.000-04:00"
categories:
  - "news"
  - "research"
  - "ai"
tags:
  - "LLM"
  - "EHR"
  - "NLP"
  - "Cardio-Oncology"
  - "Prompt Engineering"
  - "Open Source"
aliases:
  - /2026/08/31/jefferson-investigates-features-tracer/
description: "Jefferson Investigates (August 2026) covers TRACER, our open-source LLM framework that extracts cardiac event data from cancer patients' electronic health records in seconds instead of hours."
---

[Large Language Model-Based System Identifies Cardiac Event Data in Cancer Patients' Electronic Health Records (Jefferson Investigates, August 2026)](https://www.jefferson.edu/news/2026/08/aug-2026-roundup.html)

Jefferson's monthly research roundup, *Jefferson Investigates*, features our **TRACER** study, the
prompting framework that lets open-source large language models pull cardiac events out of
unstructured electronic health records. The paper appeared in the *International Journal of Radiation
Oncology, Biology, Physics* (the Red Journal).

Patients treated for breast and lung cancer carry an elevated risk of cardiotoxicity, simply because
of how close the heart sits to the treatment target. Finding evidence of that damage means reading
through hundreds of patient charts. Done by hand, that is slow enough to be impractical for most
research questions. Across the 411-patient cohort in the study, manual review took roughly two hours
per chart; the LLM pipeline took 20 to 42 seconds.

> "It took physicians, residents and students a long time to collect patients' data manually. We hope
> our study demonstrates that this process can be taken over by the large language model, to save
> time."
>
> **Wenchao Cao, PhD**, first author

Much of the difficulty is in the negatives. The prompts have to recognize that "ruled out a heart
attack" is not a cardiac event. As Dr. Cao puts it in the article, "you would be surprised to see how
many different ways there are to describe a negative situation, like 'patient denied' a certain
disease."

The article also points to where this goes next: identifying which patients are most likely to
develop cardiotoxicity, so radiation therapy plans can be individualized to reduce that risk.

For us TRACER is a starting point, not an endpoint. Turning free-text charts into structured outcome
labels at a scale manual review could never reach is what makes the next questions tractable, and
several follow-up AI studies are already building on it.

Written by Lisa Fields for Jefferson Investigates.

## Read more

- **Full study writeup:** [TRACER: Open-Source LLM Prompting Matches Specialized Medical AI for Cardiac Event Extraction](/posts/2026-07-01-tracer-open-source-llms-cardiac-event-extraction/)
- **Paper:** [10.1016/j.ijrobp.2026.06.3060](https://doi.org/10.1016/j.ijrobp.2026.06.3060) · [Red Journal](https://www.redjournal.org/article/S0360-3016(26)03913-1/fulltext)

## The team

TRACER was carried out while **Wenchao Cao, PhD** was our Senior Physics Resident. She has since
completed the residency and joined the department as **medical physics faculty** on July 1, where she
is continuing this line of research. She worked with **Nilanjan "Neel" Haldar, MD**, for whom this was
one of many projects taken on during his Jefferson Radiation Oncology residency. Much of the chart
review and validation was done by medical students from Jefferson's summer oncology program: Isis
Lloyd, Moorin Khan, Michael Dichmann, and Patrick Faherty, along with Femi Adejolu, then a Penn State
undergraduate in the Penn State/Jefferson accelerated BS/MD program. A trainee-driven project from
start to finish.
