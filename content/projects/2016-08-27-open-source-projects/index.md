---
title: "Open source projects"
date: "2026-05-20T22:00:40.000-04:00"
lastmod: "2026-11-01T19:30:00.000-05:00"
aliases:
  - /portfolio/open-source-projects/
description: "Active and legacy open-source projects from the CHOI Lab: qradiomics CLI, nexus-lite multi-agent orchestrator, loom sandboxed leaf-agent CLI, medimage Colab course, CIRDataset, and PathCNN."
---

This page summarizes active and legacy open-source projects from Choi Lab.

## Active

### [qradiomics](/qradiomics/)

Unified Python radiomics CLI (`qr`) and library for end-to-end workflows (DICOM & Enhanced PET conversion, IBSI-1 & IBSI-SUV v3.1 PET normalization, deformable registration, longitudinal contour QC, multi-engine feature extraction, 3D shape descriptors, Nextflow/Prefect orchestration, and survival/ML benchmarking).

- Repo: [github.com/choilab-jefferson/qradiomics](https://github.com/choilab-jefferson/qradiomics) · PyPI: [qradiomics](https://pypi.org/project/qradiomics/)
- Version: `0.9.6` · License: MIT
- Status: actively maintained

### [nexus-lite](/nexus-lite/)

Colab-ready, zero-server Python multi-agent orchestration kernel and scientific workflow suite (`dtach` PTYs, SQLite WAL Bus v1, 3-tier memory `stm`/`mtm`/`ltm`, parallel swarms, role pipelines, peer-to-peer A2A review loops, zero-preinstall remote compute, local Ollama GPU/CPU swarms, and 6 Google Colab notebooks).

- Repo: [github.com/choilab-jefferson/nexus.lite](https://github.com/choilab-jefferson/nexus.lite) · PyPI: [nexus-lite](https://pypi.org/project/nexus-lite/) (`pip install nexus-lite`)
- Version: `0.2.2` · License: MIT
- Status: actively maintained

### [loom](/loom/)

Zero-dependency (Go stdlib only) sandboxed single-agent leaf CLI with workspace confinement, multi-turn `loom.context.v1` piping (`--context-in`/`--context-out`), allowlisted command execution with timeout clamping (`--max-cmd-timeout`), hard turn/token/deadline budgets, `--phi` local-model enforcement, resumable JSONL traces, and 93-test IBSI radiomics verification with `nexus-lite`.

- Repo: [github.com/choilab-jefferson/nexus.loom](https://github.com/choilab-jefferson/nexus.loom)
- Version: `0.2.3` · License: MIT
- Status: actively maintained

### [medimage](/posts/2026-08-04-introducing-medimage/)

Free, 13-chapter hands-on Google Colab course in quantitative medical image analysis, covering DICOM fundamentals, CT/MR body composition, PET SUV, radiomics extraction, and end-to-end study reproduction.

- Repo: [github.com/choilab-jefferson/medimage](https://github.com/choilab-jefferson/medimage)
- License: MIT
- Status: actively maintained

## Legacy (superseded by qradiomics)

### [Lung Cancer Screening Radiomics](../2022-06-10-lung-cancer-screening-radiomics/)

Earlier end-to-end screening workflow on LIDC-IDRI and LUNGx with AutoML components.

- Repo: [github.com/choilab-jefferson/LungCancerScreeningRadiomics](https://github.com/choilab-jefferson/LungCancerScreeningRadiomics)
- Status: no longer maintained

### [Radiomics Tools](../2016-07-23-radiomics-tools/)

C++/Python (ITK, Ruffus) radiomics pipeline including DICOM/RT handling and feature extraction.

- Repo: [github.com/taznux/radiomics-tools](https://github.com/taznux/radiomics-tools)
- Status: no longer maintained

### [Lung Image Analysis Framwork](../2016-08-27-lung-image-analysis-framwork/)

MATLAB framework for pulmonary nodule detection and characterization on CT.

- Repo: [github.com/taznux/lung-image-analysis](https://github.com/taznux/lung-image-analysis)
- Status: no longer maintained

## Related

### [PathCNN](../2022-06-10-pathcnn/)

Interpretable CNN for survival prediction and pathway analysis in glioblastoma.

- Repo: [github.com/mskspi/PathCNN](https://github.com/mskspi/PathCNN)
