---
title: "Open source projects"
date: "2026-05-20T22:00:40.000-04:00"
lastmod: "2026-11-04T16:00:00.000-05:00"
aliases:
  - /portfolio/open-source-projects/
description: "Active and legacy open-source projects from the CHOI Lab: qradiomics CLI, nexus-lite multi-agent orchestrator, loom sandboxed leaf-agent CLI, medimage Colab course, CIRDataset, PathCNN, and our portable compute architecture."
---

This page summarizes active and legacy open-source software, datasets, and educational resources from the **[CHOI Lab](/about/)**. For a full synthesis of how our stack evolved from early 3D computer vision foundations (2002–2023) and our AAPM 2025 pipeline into today's unified ecosystem—and how we use portable pipelines and secured compute environments (**"Data-Stay, Pipeline-Go"**) to enable multi-center collaboration—see **[The CHOI Lab Open-Source Ecosystem Overview](/ecosystem/)**.

## Active Flagship Ecosystem

| Layer | Project | Version & License | Links | Primary Role |
| :--- | :--- | :--- | :--- | :--- |
| **1. Domain CLI & Standardized Library** | **[`qradiomics`](/qradiomics/)** | `v0.9.6` · **MIT** | [GitHub](https://github.com/choilab-jefferson/qradiomics) · [PyPI](https://pypi.org/project/qradiomics/) · [Docs](/qradiomics/) | Unified Python radiomics CLI (`qr`): TCIA automation, DICOM/RTSTRUCT/Enhanced PET conversion, **IBSI-1** & **IBSI-SUV v3.1** PET parity (58/58 DRO + 16/16 ACRIN 6668), deformable registration (`sitk`, `plastimatch`, `elastix`), `qr longitudinal` contour QC, multi-engine extraction (`pyradiomics`, `pysera`, `rtools`), 3D shape (`AHSN`, `spic6`), Nextflow/Prefect workflow assembly, and reproduction of **8 published protocols** |
| **2. Multi-Agent Orchestrator & Portable Compute** | **[`nexus-lite`](/nexus-lite/)** | `v0.2.2` · **MIT** | [GitHub](https://github.com/choilab-jefferson/nexus.lite) · [PyPI](https://pypi.org/project/nexus-lite/) · [Post](/nexus-lite/) | Colab-ready, zero-server Python multi-agent kernel (`dtach` PTYs, SQLite WAL Bus v1, 3-tier memory `stm`/`mtm`/`ltm`, parallel swarms, role pipelines, `NEXUS_SENSITIVITY=phi` local Ollama routing, zero-preinstall remote compute `nexus_lite.compute`, and **6 Google Colab notebooks**) |
| **3. Sandboxed Leaf-Agent Binary** | **[`loom`](/loom/)** | `v0.2.3` · **MIT** | [GitHub](https://github.com/choilab-jefferson/nexus.loom) · [Releases](https://github.com/choilab-jefferson/nexus.loom/releases) · [Post](/loom/) | Zero-dependency (Go 1.22+ stdlib only) single-agent leaf CLI with workspace confinement, multi-turn `loom.context.v1` piping, allowlisted command execution with timeout clamping, hard turn/token/deadline budgets, `--phi` local-only model confinement, and 93-test IBSI radiomics verification |
| **4. Open Curriculum** | **[`medimage`](/posts/2026-08-04-introducing-medimage/)** | 13 Chapters · **MIT** | [GitHub](https://github.com/choilab-jefferson/medimage) · [Post](/posts/2026-08-04-introducing-medimage/) | Free, zero-setup Google Colab course in quantitative medical image analysis from DICOM fundamentals to reproducing Aerts 2014 |
| **5. Benchmark Dataset & Spiculation** | **[`CIR` / `CIRDataset`](https://github.com/choilab-jefferson/CIR)** | 966 Nodules · Open Access | [GitHub](https://github.com/choilab-jefferson/CIR) · [Zenodo `6762573`](https://zenodo.org/records/6762573) · [arXiv](https://arxiv.org/abs/2206.14903) | Clinically interpretable lung nodule radiomics (conformal 3D spiculation and lobulation) and the *MICCAI* 2022 radiologist QA/QC'd dataset ($883$ LIDC-IDRI + $83$ LUNGx nodules) |
| **6. Domain AI Assistant** | **[Medical Physics Gem](/posts/2026-05-24-announcing-gemini-gem-for-computational-medical-physics/)** | Gemini Gem · Free | [Announcement](/posts/2026-05-24-announcing-gemini-gem-for-computational-medical-physics/) | Specialized AI co-pilot for medical image computing, radiation dosimetry, protocol QA, Monte Carlo modeling, and authoring `qradiomics` pipelines |

---

### [qradiomics](/qradiomics/)

Unified Python radiomics CLI (`qr`) and library for end-to-end workflows (DICOM & Enhanced PET conversion, IBSI-1 & IBSI-SUV v3.1 PET normalization, deformable registration, longitudinal contour QC, multi-engine feature extraction, 3D shape descriptors, Nextflow/Prefect orchestration, and survival/ML benchmarking).

- Repo: [github.com/choilab-jefferson/qradiomics](https://github.com/choilab-jefferson/qradiomics) · PyPI: [qradiomics](https://pypi.org/project/qradiomics/) (`pip install qradiomics`)
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
