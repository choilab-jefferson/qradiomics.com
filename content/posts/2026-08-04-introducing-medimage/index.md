---
title: "Introducing medimage — A Free Colab Course in Quantitative Medical Image Analysis"
date: "2026-08-04T09:00:00.000-04:00"
categories:
  - "news"
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
  alt: "medimage curriculum overview: Part I Foundations (Ch 1-5), Part II Applications (Ch 6-8), Part III Methods (Ch 9-13)"
  relative: true
---

**medimage** is a free, notebook-based course, not just a code library. Every chapter runs directly
in **Google Colab** with no local setup: open a notebook, run the cells, and you're working with real
(de-identified, publicly licensed) CT, MR, and PET data. It takes you from opening your first DICOM
file to measuring body composition on CT and MR, and finally to reproducing a published radiomics
result end to end. No prior background in medical imaging is assumed.

**License:** MIT · **Repo:** [choilab-jefferson/medimage](https://github.com/choilab-jefferson/medimage)

## Curriculum

Every card opens straight in Colab — no account setup, no local install, click and run. Each chapter
is standalone: open any single notebook and it fetches and prepares its own data, with no dependency
on another chapter having run first.

<div class="mi-part">
  <div class="mi-part-eyebrow">Part I</div>
  <h3 class="mi-part-title">Foundations</h3>
  <div class="mi-chapter-grid">
    <a class="mi-chapter" href="https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter01_Exploration.ipynb" target="_blank" rel="noopener">
      <span class="mi-chapter-num">CH. 01</span>
      <span class="mi-chapter-title">Exploration</span>
      <span class="mi-chapter-hook">DICOM, headers, Hounsfield units, orientation, viewing volumes</span>
      <span class="mi-chapter-cta">Open in Colab</span>
    </a>
    <a class="mi-chapter" href="https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter02_Masks_and_Filters.ipynb" target="_blank" rel="noopener">
      <span class="mi-chapter-num">CH. 02</span>
      <span class="mi-chapter-title">Masks and filters</span>
      <span class="mi-chapter-hook">Histograms, selecting pixels, denoising, morphology, edges</span>
      <span class="mi-chapter-cta">Open in Colab</span>
    </a>
    <a class="mi-chapter" href="https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter03_Measurement.ipynb" target="_blank" rel="noopener">
      <span class="mi-chapter-num">CH. 03</span>
      <span class="mi-chapter-title">Measurement</span>
      <span class="mi-chapter-hook">Labeling, object selection, area/volume, mean HU, validating with Dice</span>
      <span class="mi-chapter-cta">Open in Colab</span>
    </a>
    <a class="mi-chapter" href="https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter04_Image_Comparison.ipynb" target="_blank" rel="noopener">
      <span class="mi-chapter-num">CH. 04</span>
      <span class="mi-chapter-title">Image comparison</span>
      <span class="mi-chapter-hook">Resampling, transformations, similarity metrics, normalization</span>
      <span class="mi-chapter-cta">Open in Colab</span>
    </a>
    <a class="mi-chapter" href="https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter05_Patient_Privacy.ipynb" target="_blank" rel="noopener">
      <span class="mi-chapter-num">CH. 05</span>
      <span class="mi-chapter-title">Patient privacy</span>
      <span class="mi-chapter-hook">Finding, removing, and verifying removal of PHI in DICOM</span>
      <span class="mi-chapter-cta">Open in Colab</span>
    </a>
  </div>
</div>

<div class="mi-part">
  <div class="mi-part-eyebrow">Part II</div>
  <h3 class="mi-part-title">Applications</h3>
  <div class="mi-chapter-grid">
    <a class="mi-chapter" href="https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter06_Body_Composition_CT.ipynb" target="_blank" rel="noopener">
      <span class="mi-chapter-num">CH. 06</span>
      <span class="mi-chapter-title">Body composition from CT</span>
      <span class="mi-chapter-hook">Finding L3, a pretrained model, muscle / SAT / VAT, the muscle index</span>
      <span class="mi-chapter-cta">Open in Colab</span>
    </a>
    <a class="mi-chapter" href="https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter07_MR_Fat_Quantification.ipynb" target="_blank" rel="noopener">
      <span class="mi-chapter-num">CH. 07</span>
      <span class="mi-chapter-title">Fat quantification with MR</span>
      <span class="mi-chapter-hook">Dixon in/opposed-phase, fat-fraction maps, liver steatosis</span>
      <span class="mi-chapter-cta">Open in Colab</span>
    </a>
    <a class="mi-chapter" href="https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter08_PET_CT.ipynb" target="_blank" rel="noopener">
      <span class="mi-chapter-num">CH. 08</span>
      <span class="mi-chapter-title">PET/CT</span>
      <span class="mi-chapter-hook">SUV, PET/CT fusion, cardiac FDG uptake, change between timepoints</span>
      <span class="mi-chapter-cta">Open in Colab</span>
    </a>
  </div>
</div>

<div class="mi-part">
  <div class="mi-part-eyebrow">Part III</div>
  <h3 class="mi-part-title">Quantitative methods</h3>
  <div class="mi-chapter-grid">
    <a class="mi-chapter" href="https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter09_Radiomics_Features.ipynb" target="_blank" rel="noopener">
      <span class="mi-chapter-num">CH. 09</span>
      <span class="mi-chapter-title">Radiomics features</span>
      <span class="mi-chapter-hook">The three feature families, patterns, and what preprocessing does to each</span>
      <span class="mi-chapter-cta">Open in Colab</span>
    </a>
    <a class="mi-chapter" href="https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter10_Registration.ipynb" target="_blank" rel="noopener">
      <span class="mi-chapter-num">CH. 10</span>
      <span class="mi-chapter-title">Registration</span>
      <span class="mi-chapter-hook">Two engines, scoring in millimeters, diagnosing a silent failure</span>
      <span class="mi-chapter-cta">Open in Colab</span>
    </a>
    <a class="mi-chapter" href="https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter11_Delta_Radiomics.ipynb" target="_blank" rel="noopener">
      <span class="mi-chapter-num">CH. 11</span>
      <span class="mi-chapter-title">Delta radiomics</span>
      <span class="mi-chapter-hook">Measuring change between timepoints, and your own noise floor</span>
      <span class="mi-chapter-cta">Open in Colab</span>
    </a>
    <a class="mi-chapter" href="https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter12_Classification.ipynb" target="_blank" rel="noopener">
      <span class="mi-chapter-num">CH. 12</span>
      <span class="mi-chapter-title">Classification</span>
      <span class="mi-chapter-hook">Benchmarking eight models, a real data leak that scored AUC 1.000, and what a hold-out set can and cannot tell you at this size</span>
      <span class="mi-chapter-cta">Open in Colab</span>
    </a>
    <a class="mi-chapter" href="https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter13_Reproducibility.ipynb" target="_blank" rel="noopener">
      <span class="mi-chapter-num">CH. 13</span>
      <span class="mi-chapter-title">Reproducing published results</span>
      <span class="mi-chapter-hook">The full <code>qr</code> analysis on Lung1, compared against the paper</span>
      <span class="mi-chapter-cta">Open in Colab</span>
    </a>
  </div>
</div>

Each chapter teaches the failure mode alongside the technique — a registration that fails silently
and is shown side by side with the run that worked (Ch. 10), a real data leak walked through step by
step (Ch. 12), a "does the number actually add up" check before trusting it (Ch. 3) — rather than
only the happy path. Chapter 12 closes by splitting the same 59 patients six ways and getting
hold-out AUCs from 0.48 to 0.74, which is an argument about sample size rather than about models.

## Run it — no install required

Every notebook opens with a setup cell that detects Colab, clones the repo, and installs anything the
runtime is missing. Start at Chapter 1:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/choilab-jefferson/medimage/blob/main/Chapter01_Exploration.ipynb)

Local execution is also supported:

```bash
git clone https://github.com/choilab-jefferson/medimage.git
cd medimage
pip install -r requirements.txt
jupyter lab
```

Everything installs from PyPI with one exception. The four chapters that extract radiomics features
need **pyradiomics**, which publishes no wheel for Python 3.10 or newer, so it is built from its
upstream git — a few minutes on first install. In Colab that cost is paid once per session, and only
in the notebooks that need it; every other chapter installs in well under a minute. The local
`requirements.txt` above installs it up front, whichever chapters you plan to run.

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

Chapters 5, 9, 11, 12 and 13 run the same `qr` CLI that powers **[QRadiomics](/qradiomics/)**, Choi
Lab's radiomics research toolkit — Chapter 13 reproduces the Aerts 2014 NSCLC-Radiomics Cox PH result
using the public `qr extract` → `qr results merge` → `qr analyze survival` pipeline. medimage is the
teaching path into the same tools and data used in the lab's published research.

---

*Choi Lab, Department of Radiation Oncology, Sidney Kimmel Medical College at Thomas Jefferson
University* — [Wookjin Choi, Ph.D.](/profile/) · MIT License · [LICENSE](https://github.com/choilab-jefferson/medimage/blob/main/LICENSE)
