---
title: "Introducing qradiomics — A Unified Radiomics CLI for Reproducible Research"
date: "2026-05-20T17:00:00.000-04:00"
lastmod: "2026-05-20T22:12:20.000-04:00"
categories:
  - "news"
  - "research"
  - "open-source"
tags:
  - "Radiomics"
  - "Python"
  - "CLI"
  - "Lung Cancer"
  - "Open Source"
  - "PyRadiomics"
  - "TCIA"
  - "Reproducibility"
  - "LIDC-IDRI"
  - "Spiculation"
  - "PathCNN"
  - "Deep Learning"
  - "Cardiac"
  - "PET"
  - "AI Agent"
  - "Radiomics Agent"
cover:
  image: "images/qradiomics-workflow-overview.svg"
  alt: "qradiomics workflow overview"
  relative: true
aliases:
  - /2026/05/20/introducing-qradiomics/
description: "Introducing qradiomics, a unified Python CLI and library to automate radiomics research pipelines from DICOM to published-grade survival models."
---

Today, we are thrilled to announce the official release of **[qradiomics](https://github.com/choilab-jefferson/qradiomics)** — an open-source Command Line Interface (CLI) and **agent-friendly orchestrator** designed to bring reproducibility, scalability, and AI-driven automation to the world of radiomics research. It is also available on PyPI at [pypi.org/project/qradiomics](https://pypi.org/project/qradiomics/).

## What is qradiomics?

`qradiomics` (command: `qr`) is a radiomics research CLI built for the full data flow from raw DICOM to published-grade results:

```
DICOM download → conversion → feature extraction → clinical merge → modeling
```

Each step is a single Unix-style command. Pipelines are assembled from those atomic commands using plain JSON plans, executed by Nextflow (per-patient parallel), Prefect, or inline. One command gets you started:

```bash
curl -sSL https://raw.githubusercontent.com/choilab-jefferson/qradiomics/main/scripts/kickoff.sh | bash
```

## Three earlier projects, unified

`qradiomics` is the direct successor of three Choi Lab codebases that are now retired:

| Earlier project | Stack | Status |
|---|---|---|
| [taznux/lung-image-analysis](https://github.com/taznux/lung-image-analysis) | MATLAB | superseded |
| [taznux/radiomics-tools](https://github.com/taznux/radiomics-tools) | C++ / ITK / Ruffus | superseded |
| [choilab-jefferson/LungCancerScreeningRadiomics](https://github.com/choilab-jefferson/LungCancerScreeningRadiomics) | MATLAB / Python | superseded |

The feature extractors, spiculation pipeline, and LIDC-IDRI workflow from all three are now available as pure Python under a single MIT-licensed package.

## Reproducibility: published results re-confirmed

One of the primary goals of qradiomics is to make published results independently verifiable. Running the bundled pipelines on public TCIA datasets reproduces — or exceeds — the numbers from four peer-reviewed papers:

| Paper | Method | Our result | Published |
|---|---|---|---|
| Choi 2018 *Med Phys* | radiomics50 | AUC **0.872 ± 0.010** | 0.83 – 0.95 |
| Choi 2021 *CMPB* — spic6 only | 6 spiculation features | AUC **0.816 ± 0.006** | 0.80 – 0.85 |
| Choi 2021 *CMPB* — PM (CIR masks) | radiomics + spic | AUC **0.868 ± 0.039** | 0.85 |
| Choi 2021 *CMPB* — LUNGx external | radiomics50 + calibration | AUC **0.756** | 0.76 |

The LUNGx external validation result (AUC 0.756) matches the published number exactly using only interpretable hand-crafted features — no neural-network encoder required.

## Key features

- **`qr tcia download`** — bulk-pull any TCIA collection with multi-process progress
- **`qr convert dicom-series / rtstruct`** — DICOM CT/PET/MR + RTSTRUCT → NRRD (SUV-corrected for PET, case-insensitive ROI lookup)
- **`qr extract`** — PyRadiomics with bundled pattern templates (`nsclc-survival`, `ct-default`, …)
- **`qr analyze survival / classify / importance`** — Cox PH, logistic regression, random-forest feature importance
- **`qr ml train / predict / evaluate`** — leakage-safe cross-validated model building
- **`qr workflow plan / scaffold / run`** — Nextflow / Prefect / inline pipeline assembly
- **`qr anonymize`** — strip PHI from DICOM trees (PS3.15 Annex E)
- **`qradiomics.shape`** — Python re-implementations of the Choi 2014 AHSN nodule detector and Choi 2021 spiculation quantifier

## Validated on four public cohorts

The same pipeline has been validated end-to-end on TCIA data:

- **NSCLC-Radiomics (Lung1)** — Aerts 2014 discovery cohort (n=420) — open access
- **LIDC-IDRI** — full 1,018-scan reference benchmark — open access
- **NSCLC-Cetuximab** — external validation (n=460) — available via NCI data access agreement
- **ACRIN-NSCLC-FDG-PET** — PET/CT with cardiac and pulmonary ROIs — open access

## Get started

```bash
# Install from PyPI
pip install qradiomics[rtstruct]

# One-liner smoke test (synthetic data, no download required)
python scripts/smoke.py

# Full Lung1 end-to-end (~1 h on 16 cores)
qr tcia download --collection NSCLC-Radiomics --modality CT -o /data/Lung1 -j 16
```

Full documentation: [../../projects/2026-05-17-qradiomics/](../../projects/2026-05-17-qradiomics/)  
Source code: [github.com/choilab-jefferson/qradiomics](https://github.com/choilab-jefferson/qradiomics)

---

## Broader Choi Lab research — all publicly available

`qradiomics` is the computational backbone, but the lab's research portfolio covers several active fronts. All of the following are fully public.

### Interpretable spiculation quantification (Choi 2021, *CMPB*)

A reproducible, geometry-based algorithm for quantifying nodule spiculation in CT — one of the most diagnostically important features for lung cancer malignancy assessment. Available as `qradiomics.shape`. Paper: [doi:10.1016/j.cmpb.2020.105839](https://doi.org/10.1016/j.cmpb.2020.105839).

### Functional radiomics: cardiac PET in lung cancer RT (Choi 2023 / 2024)

A novel functional radiomics method that uses serial cardiac FDG-PET uptake as a surrogate of radiation-induced cardiotoxicity. Featured in a *JCO Clinical Cancer Informatics* editorial.  
Posts: [Novel Functional Delta-Radiomics (AAPM/ASTRO 2023)](../2023-09-11-novel-functional-delta-radiomics-for-predicting-overall-survival-in-lung-cancer-radiotherapy-using-cardiac-fdg-pet-uptake/) · [JCO CCI editorial (2024)](../2024-04-14-shining-a-light-unveiling-cardiac-risks-using-pet-imaging-in-lung-cancer-radiotherapy/)

---

## Looking back — and forward

The first radiomics code from this lab was written in **MATLAB in 2012**. Since then, the stack evolved through C++/ITK (radiomics-tools), through separate MATLAB+Python scripts (LungCancerScreeningRadiomics), and is now a single Python package with automated pipelines, leakage-safe modeling, and full TCIA integration.

The pipeline was first presented publicly at **AAPM 2025** (Washington, DC, Jul 27), validated on 207 institutional lung cancer patients (340 GTVs) and the TCIA NSCLC-Radiomics (Lung1) cohort (422 patients). The study demonstrated end-to-end automation — CT/RTSTRUCT/RTDOSE conversion, PyRadiomics extraction, and Prefect-orchestrated inference — processing the full Lung1 dataset in under 20 minutes:

> Bhetwal P, Dichmann M, Ghimire R, Chen Y, Vinogradskiy Y, Werner-Wasik M, Dicker A, **Choi W**.  
> *Development and Validation of a Scalable Radiomics Pipeline for Lung Cancer Research Using Clinical and Public Datasets* (SU-1015-202-4).  
> **Medical Physics** 52(10):e700597, AAPM 2025.

A companion study presented at **ASTRO 2025** applied the same pipeline to survival modeling across a 629-patient multi-institutional cohort (207 institutional + 422 TCIA Lung1), combining clinical and radiomic features with Cox PH models. Integrating radiomics with clinical variables improved overall survival prediction from C-index 0.50–0.56 (clinical-only) to **0.57–0.69**. The institutional portion uses private clinical data; the TCIA Lung1 component is fully reproducible with qradiomics:

> Bhetwal P, Dichmann M, Ghimire R, Chen Y, Vinogradskiy Y, Werner-Wasik M, Dicker AP, **Choi W**.  
> *Integrating Clinical and Radiomic Features for Enhanced Prognostic Modeling for Lung Cancer Survival*.  
> **IJROBP** 123(1):e719, ASTRO 2025. [doi:10.1016/S0360-3016(25)03724-1](https://www.redjournal.org/article/S0360-3016(25)03724-1/abstract)

The open-source release arrives roughly nine months after those presentations. The public release of `qradiomics` marks the point where reproducibility is no longer an afterthought — every result in our past papers can be re-run with one command on publicly available data.

Full documentation: [../../projects/2026-05-17-qradiomics/](../../projects/2026-05-17-qradiomics/)  
Source code: [github.com/choilab-jefferson/qradiomics](https://github.com/choilab-jefferson/qradiomics)

---

*Choi Lab, Department of Radiation Oncology, Sidney Kimmel Medical College at Thomas Jefferson University.*
