---
title: "medimage — Quantitative Medical Image Analysis with Python"
date: "2026-08-04T07:00:00.000-04:00"
categories:
  - "research"
  - "open-source"
tags:
  - "Radiomics"
  - "Python"
  - "DICOM"
  - "Education"
  - "Google Colab"
  - "CT"
  - "MR"
  - "PET"
description: "medimage is a free, hands-on Colab course from Choi Lab — 13 notebook chapters from opening a DICOM file to CT/MR body composition, PET SUV, radiomics, and reproducing a published study."
cover:
  image: "images/medimage-overview.svg"
  alt: "medimage curriculum overview: Part I Foundations (Ch 1-5), Part II Applications (Ch 6-8), Part III Quantitative methods (Ch 9-13)"
  relative: true
---

**License:** MIT · **Repo:** [choilab-jefferson/medimage](https://github.com/choilab-jefferson/medimage)

**medimage** is a free, notebook-based course — not just a code library. Every chapter runs directly
in **Google Colab** with no local setup: open a notebook, run the cells, and you're working with real
(de-identified, publicly licensed) CT, MR, and PET data. It takes you from opening your first DICOM
file to measuring body composition on CT and MR, and finally to reproducing a published radiomics
result end to end. No prior background in medical imaging is assumed — each chapter builds directly
on what came before it.

## Curriculum

Every row opens straight in Google Colab — no account setup, no local install, click and run.

| Chapter | What you learn | Why the course needs it | |
|---|---|---|---|
| **Part I — Foundations** | | | |
| 1. Exploration | DICOM, headers, Hounsfield units, image orientation, viewing volumes | You cannot measure anything until the numbers mean something | [Open →](https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter01_Exploration.ipynb) |
| 2. Masks and filters | Histograms, selecting pixels, denoising, morphology, edges | Fat and muscle are picked out by their HU range — after denoising | [Open →](https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter02_Masks_and_Filters.ipynb) |
| 3. Measurement | Labeling, object selection, area and volume, mean HU, validating with Dice | Areas and mean HU *are* the body composition numbers | [Open →](https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter03_Measurement.ipynb) |
| 4. Image comparison | Resampling, transformations, similarity metrics, normalization | Two patients are different sizes, so raw numbers cannot be compared | [Open →](https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter04_Image_Comparison.ipynb) |
| 5. Patient privacy | Finding, removing, and **verifying** removal of PHI in DICOM | Before any of this can touch real clinical data | [Open →](https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter05_Patient_Privacy.ipynb) |
| **Part II — Applications** | | | |
| 6. Body composition from CT | Finding L3, verifying a pretrained model, muscle / SAT / VAT, the muscle index | The destination the first four chapters were building toward | [Open →](https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter06_Body_Composition_CT.ipynb) |
| 7. Fat quantification with MR | Dixon in/opposed-phase, fat-fraction maps, liver steatosis | The other modality that can measure fat, and why CT is still the default | [Open →](https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter07_MR_Fat_Quantification.ipynb) |
| 8. PET/CT | SUV, PET/CT fusion, cardiac FDG uptake, change between timepoints | Function as well as anatomy — and a published clinical application | [Open →](https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter08_PET_CT.ipynb) |
| **Part III — Quantitative methods** | | | |
| 9. Radiomics features | The three feature families, patterns, and what preprocessing does to each | Knowing which of your ~1,130 features survive someone else running the pipeline | [Open →](https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter09_Radiomics_Features.ipynb) |
| 10. Registration | Two engines, scoring in millimeters, diagnosing a registration that fails silently | Aligning scans is where pipelines break without saying so | [Open →](https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter10_Registration.ipynb) |
| 11. Delta radiomics | Measuring change between timepoints, and your own noise floor | Change is more informative than any single value — once you know what change means | [Open →](https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter11_Delta_Radiomics.ipynb) |
| 12. Classification | Benchmarking eight models, and a real data leak that produced AUC 1.000 | An implausibly good result is a bug report, not a finding | [Open →](https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter12_Classification.ipynb) |
| 13. Reproducing published results | The full `qr` analysis on Lung1, compared against the paper | Whether a pipeline reproduces is the question that matters | [Open →](https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter13_Reproducibility.ipynb) |

Each chapter teaches the failure mode alongside the technique — a registration that fails silently
(Ch.10), a real data leak walked through step by step (Ch.12), a "does the number actually add up"
check before trusting it (Ch.3) — rather than only the happy path.

## Run it — no install required

Every notebook opens with a setup cell that detects Colab, clones the repo, and installs anything the
runtime is missing. Each chapter is standalone — open any single notebook in Colab and it fetches and
prepares its own data, with no dependency on another chapter having been run first. Start at Chapter 1:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter01_Exploration.ipynb)

Local execution is also supported:

```bash
git clone https://github.com/choilab-jefferson/medimage.git
cd medimage
pip install -r requirements.txt
jupyter lab
```

## No imaging data in the repo

Every notebook downloads what it needs from its original public source on first run and caches it
locally (git-ignored); each loader prints its citation when it runs. That keeps the repo small and
the licensing clean — and it keeps the provenance of every image one function call away.

| Dataset | Used by | Source | License |
|---|---|---|---|
| Pancreas-CT | Ch 1–6 | [TCIA](https://doi.org/10.7937/K9/TCIA.2016.tNB1kqBU) | CC BY 3.0 |
| CHAOS (T1-DUAL MRI) | Ch 3, 7 | [Zenodo](https://doi.org/10.5281/zenodo.3431873) | CC BY-NC-SA 4.0 |
| ACRIN-NSCLC-FDG-PET (ACRIN 6668) | Ch 8, 11 | [TCIA](https://www.cancerimagingarchive.net/collection/acrin-nsclc-fdg-pet/) | TCIA data usage policy |
| NSCLC-Radiomics (Lung1) | Ch 9, 12, 13 | [TCIA](https://www.cancerimagingarchive.net/collection/nsclc-radiomics/) | CC BY-NC 3.0 |

## Built alongside QRadiomics

The final chapters (9, 12, 13) run the same `qr` CLI that powers **[QRadiomics](/qradiomics/)**, Choi
Lab's radiomics research toolkit — Chapter 13 reproduces the Aerts 2014 NSCLC-Radiomics Cox PH result
using the public `qr extract` → `qr results merge` → `qr analyze survival` pipeline. medimage is the
teaching path into the same tools and data used in the lab's published research.

## Authors

*Choi Lab, Department of Radiation Oncology, Sidney Kimmel Medical College at Thomas Jefferson
University* — [Wookjin Choi, Ph.D.](/profile/)

## License

MIT — see [LICENSE](https://github.com/choilab-jefferson/medimage/blob/main/LICENSE).
