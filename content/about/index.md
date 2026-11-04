---
title: "About the Lab"
date: "2026-06-05T15:22:00.000-04:00"
lastmod: "2026-11-04T16:00:00.000-05:00"
description: "The Computational Healthcare & Oncology Informatics (CHOI) Lab at Thomas Jefferson University: our past foundations in 3D computer vision, present open-source radiomics & clinical AI stack, and future vision for contour-robust, portable clinical AI."
schema: "about"
---

# **Computational Healthcare & Oncology Informatics (CHOI) Lab**

Welcome to the **Computational Healthcare & Oncology Informatics (CHOI) Lab**, located within the Department of Radiation Oncology at the Sidney Kimmel Medical College & Comprehensive Cancer Center, Thomas Jefferson University.

Led by **[Wookjin Choi, Ph.D.](/profile/)** (Associate Professor of Radiation Oncology), our lab operates at the intersection of medical physics, 3D computer vision, and oncology informatics. We build mathematically interpretable ("glass-box") biomarkers, standardized radiomics pipelines, and sandboxed multi-agent AI systems to improve cancer diagnosis, guide adaptive radiation therapy, and predict treatment outcomes.

> **Read our comprehensive overview:** [**The CHOI Lab Open-Source Ecosystem: Past Foundations, Present Unification, and the Future of Portable, Contour-Robust Clinical AI**](/ecosystem/)

---

## **Laboratory Mission**

Our mission is to bridge the gap between computational innovation and routine clinical care through three guiding principles:
1. **Glass-Box Interpretability:** Designing physically and biologically grounded biomarkers—such as 3D surface-normal geometry, conformal spiculation, functional organ-at-risk remodeling, and pathway-informed neural networks—that clinicians can inspect, troubleshoot, and trust.
2. **End-to-End Reproducibility:** Releasing open-source, IBSI-standardized software packages—led by our flagship **[QRadiomics CLI](/qradiomics/)** (`v0.9.6`), **[nexus-lite](/nexus-lite/)** (`v0.2.2`) multi-agent orchestrator, **[loom](/loom/)** (`v0.2.3`) sandboxed leaf-agent CLI, and **[medimage](/posts/2026-08-04-introducing-medimage/)** 13-chapter Colab course—under the [CHOI Lab GitHub Organization (`choilab-jefferson`)](https://github.com/choilab-jefferson).
3. **"Data-Stay, Pipeline-Go" Portable Compute:** Enabling multi-institutional collaboration not by moving sensitive patient data across hospital firewalls, but by shipping portable pipelines and self-contained, secured computing environments directly to where clinical data resides.

---

## **1. What We Have Done (Foundations: 2002–2023)**

Our current platform builds on two decades of foundational work in 3D medical image computing, computer-aided diagnosis (CAD), and multi-omics modeling:

* **3D Shape & Surface-Normal Radiomics (`AHSN`):** Formulated the 180-dimensional Angular Histogram of Surface Normals (`AHSN`, *CMPB* 2014) and multi-scale Hessian filters for automated pulmonary nodule detection.
* **Low-Dose CT Lung Cancer Screening (`radiomics50`):** Established a compact, reproducible radiomic signature for early lung cancer detection (*Medical Physics* 2018 **Editor's Pick**; LUNGx Challenge Top Performer; Kaggle Data Science Bowl 2017 Bronze Medal).
* **Conformal 3D Spiculation (`spic6`) & `CIRDataset`:** Developed conformal spherical parameterization area-distortion metrics to quantify nodule spiculation (*CMPB* 2021) and published **[CIRDataset](https://github.com/choilab-jefferson/CIR)** (*MICCAI* 2022; Zenodo `6762573`), providing **966 radiologist QA/QC'd nodule masks** (883 LIDC-IDRI + 83 LUNGx).
* **Pathway-Grounded Deep Learning & 4D-CT Simulation:** Created **[PathCNN](https://github.com/mskspi/PathCNN)** (*Bioinformatics / ISMB* 2021) to fuse multi-omics biological pathway graphs with CNNs for glioblastoma survival prediction, and patented patient-specific contrast-enhanced 4D-CT simulation (*Medical Physics* 2016; U.S. Patent `9,456,798 B2` among 5 issued patents).

---

## **2. What We Are Doing (Present: 2024–2026)**

Today, the CHOI Lab has unified its legacy MATLAB and C++ codebases into a modern, four-layer open-source ecosystem while translating quantitative imaging and clinical LLMs into radiation oncology practice:

### **A. Unified Open-Source Software & Education Stack**
* **[`qradiomics`](/qradiomics/) (`qr` CLI `v0.9.6`, MIT, [PyPI](https://pypi.org/project/qradiomics/)):** End-to-end radiomics CLI and Python library featuring TCIA automation, DICOM/RTSTRUCT/Enhanced PET conversion, **100% IBSI-1 & IBSI-SUV v3.1 PET parity** (58/58 DRO + 16/16 ACRIN 6668), deformable registration (`sitk`, `plastimatch`, `elastix`), longitudinal contour QC (`qr longitudinal`), multi-engine extraction (`pyradiomics`, `pysera`, `rtools`), 3D shape (`AHSN`, `spic6`), Nextflow/Prefect workflow scaffolding, and reproduction of **8 published studies** out of the box.
* **[`nexus-lite`](/nexus-lite/) (`v0.2.2`, MIT, [PyPI](https://pypi.org/project/nexus-lite/)):** Zero-server Python multi-agent orchestration kernel (`dtach` PTYs, SQLite WAL Bus v1, 3-tier memory `stm`/`mtm`/`ltm`, `NEXUS_SENSITIVITY=phi` local Ollama routing, zero-preinstall remote compute `nexus_lite.compute`, and **6 interactive Google Colab notebooks**).
* **[`loom`](/loom/) (`v0.2.3`, MIT, [GitHub](https://github.com/choilab-jefferson/nexus.loom)):** Zero-dependency Go stdlib single-agent leaf CLI with strict workspace sandboxing, allowlisted command execution, hard turn/token/time budgets, `loom.context.v1` piping, and `--phi` local-only model confinement.
* **[`medimage`](/posts/2026-08-04-introducing-medimage/) & [Computational Medical Physicist Gem](/posts/2026-05-24-announcing-gemini-gem-for-computational-medical-physics/):** Free 13-chapter hands-on Google Colab course and specialized Gemini AI co-pilot for medical physics and radiomics.

### **B. Core Clinical Research Pillars**
1. **Longitudinal CBCT & Early Adaptive Lung Radiotherapy:** Fusing longitudinal cone-beam CT (CBCT) delta-radiomics trajectories with hierarchical spatial-temporal progressive denoising ([AAPM 2026 SNAP Oral](/posts/2026-07-06-8-abstracts-accepted-aapm-2026/)) and clinical variables to guide early adaptive interventions—recognized with the **[2026 ASTRO Basic Transitional Award in Physics](/posts/2026-07-27-2026-astro-annual-meeting-abstract-award/)** (*IJROBP* 126(1) S91).
2. **Cardiotoxicity & Thoracic Toxicity Prediction (PET & 4DCT):** Quantifying pre/post-treatment cardiac $^{18}\text{F-FDG}$ PET/CT remodeling (*JCO Clinical Cancer Informatics* 2024; ASTRO 2026 `S296`; AAPM 2026 `SU-315-GPD-R-23`) and 4DCT ventilation/perfusion biomarkers (*Radiotherapy and Oncology* 2025) to predict radiation-induced cardiac and pulmonary toxicity.
3. **Clinical LLMs (`TRACER`) & Automated Oncology Workflows:** Developing **[TRACER](/posts/2026-07-01-tracer-open-source-llms-cardiac-event-extraction/)** (*IJROBP* 2026, in press; featured in [*Jefferson Investigates*](/posts/2026-08-31-jefferson-investigates-features-tracer/)) to extract cardiac events from unstructured EHRs in **20–42 seconds per chart vs. ~2 hours manually**, alongside multi-tier **TG-263 RAG-LLM contour standardization** (`AAPM 2026 SU-115-220-8`) and high-risk bone metastasis LLM triage (*IJROBP* 2026 `e412`).
4. **MR-Guided Adaptive Radiotherapy (MRI-Linac) & Enterprise Physics QA:** Advancing computer-vision tumor tracking for MR-guided radiotherapy (*IJROBP* 2026 `e265`), population-based plan quality scoring (*IJROBP* 2026 `e231`), automated MPPG5b beam validation, and vendor-agnostic treatment plan QA (`AAPM 2026`).

---

## **3. What We Aim to Do (Future Horizon: 2026–2030+)**

Our next strategic phase addresses the remaining structural bottlenecks to widespread clinical adoption:

1. **Overcoming Contour Dependency (From Contour Hygiene to Contour-Free Clinical AI):** Reducing reliance on labor-intensive manual contours through pre-extraction longitudinal contour QC (`qr longitudinal`), intraclass correlation (`ICC`) feature stability gates, boundary-robust 3D geometric descriptors, and **contour-free diagnostic-to-treatment AI**—such as predicting patient-specific SBRT dose distributions directly from diagnostic PET/CT scans before simulation or manual contouring begins.
2. **Scaling Multi-Center Research via Portable Pipelines & Secured Compute ("Data-Stay, Pipeline-Go"):** Empowering collaborating hospitals to run standardized `qradiomics` workflows (`plan.json`) inside hermetic, network-isolated execution sandboxes (`loom --phi`, local Ollama LLMs, and containerized airlocks) or zero-setup cloud runtimes (Google Colab / DevContainers)—keeping raw PHI strictly on-premises while exchanging only verified, calibrated scientific outputs.
3. **Principled Multi-Modal AI Embeddings & Cyber-Resilient Oncology:** Building on our participation in the **[NCI AI Embeddings Innovation Lab](/posts/2026-07-27-selected-nci-ai-embeddings-innovation-lab/)** (July 2026) and our active **NIH/AHRQ R18 grant (`R18HS030060`, 2024–2029)**, we aim to fuse radiology (`qradiomics`), pathology, genomics (`PathCNN`), and EHR trajectories (`TRACER`) into unified diagnostic embeddings while engineering ransomware-resilient radiation oncology infrastructure.

---

## **Collaborations & Funding**
Our research is translated in close collaboration with clinical colleagues at the Sidney Kimmel Comprehensive Cancer Center and is supported by extramural grants and industry partnerships including the **NIH / AHRQ (`R18HS030060`)**, **Varian Medical Systems**, and **ViewRay Technologies**.

---

## **Contact Information**
* **Department:** Department of Radiation Oncology, Sidney Kimmel Medical College, Thomas Jefferson University
* **Address:** Philadelphia, PA 19107, USA
* **Email:** [Wookjin.Choi@jefferson.edu](mailto:Wookjin.Choi@jefferson.edu)
* **GitHub Organization:** [choilab-jefferson](https://github.com/choilab-jefferson)
* **Notion Workspace:** [Wookjin's Notion Workspace](https://choiw.notion.site/)
* **Slack Workspace:** [radiomics.slack.com](https://radiomics.slack.com/)
