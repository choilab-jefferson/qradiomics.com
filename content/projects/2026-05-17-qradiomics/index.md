---
title: "qradiomics — Radiomics Research CLI"
date: "2026-05-17T20:31:21.000-04:00"
lastmod: "2026-05-20T00:00:00.000-04:00"
categories:
  - "research"
tags:
  - "Radiomics"
  - "Python"
  - "CLI"
  - "PyRadiomics"
  - "Nextflow"
  - "Workflow"
  - "Lung"
  - "NSCLC"
  - "Survival"
  - "Spiculation"
  - "Shape"
  - "TCIA"
  - "DICOM"
aliases:
  - /portfolio/qradiomics/
description: "qradiomics is an open-source CLI and library for reproducible radiomics research, supporting PyRadiomics, TCIA dataset automation, and survival analysis."
---

**License:** MIT · **Python:** 3.11+ · **Version:** 0.9.0 · **Repo:** [choilab-jefferson/qradiomics](https://github.com/choilab-jefferson/qradiomics) · **PyPI:** [qradiomics](https://pypi.org/project/qradiomics/)

> **Active successor for three earlier Choi Lab radiomics codebases.** The C++/MATLAB pipelines in
> [taznux/radiomics-tools](https://github.com/taznux/radiomics-tools),
> [taznux/lung-image-analysis](https://github.com/taznux/lung-image-analysis), and
> [choilab-jefferson/LungCancerScreeningRadiomics](https://github.com/choilab-jefferson/LungCancerScreeningRadiomics)
> are **superseded** by this repo. The feature extractors are now in
> `qradiomics.feature.rtools` (Python ITK port, numerically exact to the C++ binary).
> New work should land here.

Radiomics research CLI. `qr` does two things equally well:

1. **Atomic tasks** — convert DICOM, extract features, merge clinical, fit a model. Each is a single command, files in / files out.
2. **Workflow assembly** — generate, mutate, scaffold, and run multi-step pipelines from those atomic tasks. Default executor is **Nextflow** (per-patient parallel + cache + HPC); **Prefect** is the secondary executor; `inline` is the small-cohort fallback.

The canonical radiomics data flow has four stages — `data → image → features → modeling` — and one `qr workflow plan` call instantiates the whole chain:

```bash
# Atomic tasks
qr convert dicom-series / rtstruct / manifest-from-dir
qr extract        -m manifest.csv -p <pattern> -o features.csv
qr results merge  -f features.csv -c clinical.csv -o analysis_ready.csv
qr analyze {survival,classify,importance} -i analysis_ready.csv ...
qr ml {train,predict,evaluate} ...

# Workflow assembly
qr workflow plan      -t dicom_to_ml -d <cohort> -c <clinical> -o plan.json
qr workflow scaffold  -p plan.json -e nextflow   -o pipeline.nf
qr workflow run       plan.json --executor nextflow   # default
```

## Kick-off

Single backend (`scripts/kickoff.sh`) for both flows. It clones the repo (if not already), creates a `.venv`, `pip install -e .`, runs `qr info`, and runs the smoke tests.

**One-liner install:**

```bash
curl -sSL https://raw.githubusercontent.com/choilab-jefferson/qradiomics/main/scripts/kickoff.sh | bash
```

Env knobs: `QR_REPO_URL`, `QR_REPO_DIR`, `QR_BRANCH`, `QR_PYTHON`, `QR_VENV` (set to `-` to skip the venv), `QR_SKIP_SMOKE=1` to skip pytest.

## Background — three earlier projects, unified

`qradiomics` is the modern Python successor of three earlier Choi Lab radiomics codebases. The MATLAB pipelines, the ITK / Ruffus C++ tools, and the Docker-based screening workflow are distilled here into a single Click CLI built on PyRadiomics, scikit-learn, and lifelines:

| Earlier project | Stack | Role | Status |
|---|---|---|---|
| [taznux/lung-image-analysis](https://github.com/taznux/lung-image-analysis) | MATLAB · MIT | LIDC-IDRI nodule detection / segmentation / characterization | superseded |
| [taznux/radiomics-tools](https://github.com/taznux/radiomics-tools) | C++/Python (ITK, Ruffus) · MIT | DICOM tools, GrowCut segmentation, feature extraction pipeline | superseded |
| [choilab-jefferson/LungCancerScreeningRadiomics](https://github.com/choilab-jefferson/LungCancerScreeningRadiomics) | MATLAB / Python · GPL-3.0 | LIDC + LUNGx end-to-end screening workflow with AutoML | superseded (re-implemented under MIT using PyRadiomics) |

The AHSN shape descriptor pipeline (CMPB 2014) and the spiculation quantification pipeline (CMPB 2021, companion to [choilab-jefferson/CIR](https://github.com/choilab-jefferson/CIR)) are re-integrated in `qradiomics.shape`. The longitudinal CBCT / delta-radiomics workflows (ASTRO / AAPM 2026) will be released here after publication.

## Install

```bash
pip install qradiomics            # core CLI + library from PyPI
pip install qradiomics[rtstruct]  # plus rt-utils for `qr convert rtstruct`
```

Or for development (editable mode):
```bash
git clone https://github.com/choilab-jefferson/qradiomics.git
cd qradiomics
pip install -e .
```

Python 3.11 or newer is required. PyRadiomics, SimpleITK, lifelines, scikit-learn, statsmodels, scipy, and pandas are pulled in as dependencies.

After install, `qr`, `qradiomics`, and `qrdx` are available on `$PATH` and point at `qradiomics.cli.main:cli`.

## DICOM Conversion

Many TCIA cohorts ship as DICOM (CT/PET/MR series + RTSTRUCT). Two helpers convert into the NRRD form the rest of the pipeline consumes:

```bash
# 1. CT/PET/MR DICOM series → single NRRD volume (PT auto-routes through SUV conversion)
qr convert dicom-series \
  -i <dataset_root>/<patient>/<study>/CT/ \
  -o <out>/<patient>_CT.nrrd

# 2. RTSTRUCT contour → binary label NRRD (same geometry as the reference CT)
qr convert rtstruct \
  -d <dataset_root>/<patient>/<study>/CT/ \
  -r <dataset_root>/<patient>/<study>/RTSeries/RS.<uid>.dcm \
  --roi GTV \
  -o <out>/<patient>_GTV-label.nrrd

# 3. (Optional) build a manifest by globbing image/mask pairs in a tree
qr convert manifest-from-dir \
  -d <out>/ \
  --image-glob '*_CT.nrrd' \
  --mask-glob '*-label.nrrd' \
  -o manifest.csv
```

RTSTRUCT conversion uses `rt-utils` (install via `pip install qradiomics[rtstruct]`). ROI lookup is case-insensitive. The mask is auto-reshaped to the CT geometry, with a ±1-slice z-axis trim/pad when the structure set references slices outside the series.

## End-to-end Example — TCIA NSCLC-Radiomics (Lung1) from scratch

Starts from nothing — pulls DICOM straight from TCIA, converts, extracts, joins clinical, and reports the Cox PH ranking.

```bash
# 0. One-time: install + workspace
pip install -e .[rtstruct]
export USER_DATA=/data/$USER          # ≥ 30 GB free for Lung1 (~422 patients)
mkdir -p $USER_DATA/{Lung1,Lung1-out}

# 1. DICOM pull from TCIA
qr tcia download \
  --collection NSCLC-Radiomics --modality CT \
  -o $USER_DATA/Lung1 -j 16
qr tcia download \
  --collection NSCLC-Radiomics --modality RTSTRUCT \
  -o $USER_DATA/Lung1 -j 16

# 2. DICOM → NRRD per patient: CT volume + GTV-1 binary mask
for pat in $USER_DATA/Lung1/*/; do
  pid=$(basename "$pat")
  qr convert dicom-series \
    -i  "$pat"*/CT \
    -o  "$USER_DATA/Lung1-out/${pid}_CT.nrrd"
  qr convert rtstruct \
    -d  "$pat"*/CT \
    -r  "$pat"*/RTSeries/*.dcm \
    --roi GTV-1 \
    -o  "$USER_DATA/Lung1-out/${pid}_GTV-label.nrrd"
done

# 3. Manifest
qr convert manifest-from-dir \
  -d "$USER_DATA/Lung1-out" \
  --image-glob '*_CT.nrrd' \
  --mask-glob  '*_GTV-label.nrrd' \
  -o  "$USER_DATA/Lung1-out/manifest.csv"

# 4. Feature extraction (~1130 features per patient)
qr extract \
  -m "$USER_DATA/Lung1-out/manifest.csv" \
  -p nsclc-survival \
  -o "$USER_DATA/Lung1-out/features.csv"

# 5. Join clinical + Cox PH
curl -sLo "$USER_DATA/Lung1-out/clinical.csv" \
  "https://www.cancerimagingarchive.net/wp-content/uploads/NSCLC-Radiomics-Lung1.clinical-version3-Oct-2019.csv"
qr results merge \
  -f "$USER_DATA/Lung1-out/features.csv" \
  -c "$USER_DATA/Lung1-out/clinical.csv" \
  --clinical-id-col PatientID \
  --time-col Survival.time --event-col deadstatus.event \
  -o "$USER_DATA/Lung1-out/analysis_ready.csv"
qr analyze survival \
  -i "$USER_DATA/Lung1-out/analysis_ready.csv" \
  --outcome OS_months --event OS_event \
  -o "$USER_DATA/Lung1-out/cox_results.csv"
```

Expected outcome on Lung1 (≈ 420 patients): `original_ngtdm_Busyness` ranks at the top (HR ≈ 1.23, p < 1e-4), replicating the headline finding from the Aerts 2014 *Nature Communications* paper. A full run takes ≈ 1 h on a 16-core workstation. For a 5-patient smoke run on synthetic NRRD (no download required), see `scripts/smoke.py`.

The exact same sequence is bundled per cohort under `pipelines/lung1/`, `pipelines/lidc_idri/`, `pipelines/nsclc_cetuximab/`, and `pipelines/acrin_heart/`.

## Deployable Pipelines

For each TCIA-public cohort, `pipelines/` ships a ready-to-run bundle: `plan.json` + `main.nf` + `prefect_flow.py` + `nextflow.config` + `deploy.sh`. Run any cohort end-to-end with:

```bash
cd pipelines/lung1/
cp /path/to/your/clinical.csv clinical/clinical.csv
./deploy.sh                       # nextflow (per-patient parallel, default)
EXECUTOR=prefect ./deploy.sh      # via Prefect 2.x
EXECUTOR=inline ./deploy.sh       # sequential subprocess (smoke tests)
```

Available bundles: `lung1/`, `nsclc_cetuximab/`, `lidc_idri/`, `acrin_heart/`.

## Workflow Assembly

The canonical four-stage data flow is encoded in the template library that `qr workflow plan` draws from:

| Template | Stages covered | When to use |
|---|---|---|
| `nrrd_survival` | data → features → modeling | cohort already in NRRD form |
| `dicom_survival` | data → image → features → modeling | cohort ships as DICOM + RTSTRUCT |
| `dicom_to_ml` | data → image → features → modeling (ML) | full end-to-end DICOM → trained model + CV metrics + held-out evaluation |

```bash
qr workflow plan -t dicom_to_ml \
    -d /data/cohort -c clinical.csv \
    --roi GTV --pattern nsclc-survival \
    -o plan.json
qr workflow scaffold -p plan.json -e nextflow -o pipeline.nf
qr workflow run plan.json
```

The plan is plain JSON/YAML — agents can read, mutate, and re-run without re-templating.

## Agentic Radiomics: Beyond the CLI

As the field of medical physics shifts towards AI-driven automation, `qradiomics` is designed to be more than just a tool for humans; it is built to be the **engine for a Radiomics Agent**.

### Why qradiomics is "Agent-Ready":
*   **Structured I/O:** Every command supports JSON output, allowing LLM-based agents to parse results and make autonomous decisions.
*   **Workflow Scaffolding:** Agents can generate complex Nextflow or Snakemake pipelines by simply describing the desired study design in natural language.
*   **Self-Correction:** If a feature extraction fails due to DICOM header inconsistencies, the CLI provides structured error codes that an AI agent can use to suggest (or apply) data cleaning fixes.
*   **Integration with Gemini Gems:** Our specialized [Medical Physics Gem](/posts/2026-05-24-announcing-gemini-gem-for-computational-medical-physics/) is pre-trained on `qradiomics` syntax, acting as a high-level **Radiomics Agent** that can write and execute your research code.

## Reproducibility — Published Paper Results

Full report: [`reports/reproducibility.md`](https://github.com/choilab-jefferson/qradiomics/blob/main/reports/reproducibility.md) · version 2.0 · last updated 2026-05-19

All results produced with qradiomics-public alone (no MATLAB, no Docker). Cohorts: TCIA NSCLC-Radiomics (Lung1), LIDC-IDRI (1,018 scans), LUNGx/SPIE-AAPM, CIRDataset (Zenodo 6762573).

### Summary

| Paper | Cohort | Method | Our result | Paper | Verdict |
|---|---|---|---|---|---|
| Aerts 2014 | Lung1 (n=420) | Cox PH 5-fold CV | c-index **0.580 ± 0.029** | 0.65 | ✓ within 0.07 |
| Aerts 2014 — external | Lung1 → NSCLC-Cetuximab (n=460) | Aerts signature transfer | c-index **0.562** | 0.69 | ✓ signal transfers |
| Choi 2014 CMPB — AHSN | LIDC-IDRI 1,018 (33,108 candidates) | AHSN + RF patient-grouped 5-fold | AUC **0.727 ± 0.005** | 0.85–0.93 | ✓ AHSN signal validated |
| Choi 2018 Med Phys | LIDC-IDRI 4,248 nodules | radiomics50 | AUC **0.872 ± 0.010** | 0.83–0.95 | ✓ in range |
| Choi 2021 CMPB — spic6 | LIDC-IDRI 4,248 nodules | spic6 (Np/Na/Nl/Na_att/s1/s2) | AUC **0.816 ± 0.006** | 0.80–0.85 | ✓✓ exact |
| Choi 2021 CMPB — PM (CIR masks) | LIDC-PM 72 patients, 474 nodules | radiomics+spic | AUC **0.868 ± 0.039** | 0.85 | ✓✓ exceeds |
| Choi 2021 CMPB — LUNGx ext + cal | LUNGx 60-test + 10-cal | radiomics50 CIR mask | AUC **0.756** | 0.76 | ✓✓ exact |
| Choi 2022 MICCAI / CIRDataset | LIDC-PM 72 + LUNGx 73 | interpretable, no NN encoder | AUC 0.755–0.868 | 0.813/0.743 | ✓✓ matches/exceeds |

**Three of four targeted Choi reproductions land at or above the paper's published numbers** using qradiomics-public's atomic core and the CIRDataset masks.

### Cohorts used

| Cohort | Source | Patients | Nodules | Note |
|---|---|--:|--:|---|
| Lung1 / NSCLC-Radiomics | TCIA | 420 | 420 GTV-1 | Aerts 2014 discovery cohort |
| NSCLC-Cetuximab / RTOG-0617 | local DICOM | 489 | PTV-based | external for Aerts |
| **LIDC-IDRI** (full reference) | TCIA + LIDC-XML | **1,018** | 4,248 (≥8 voxel) | 7 institutions, 8 vendors |
| **LIDC-PM** | LIDC-IDRI subset | **72** | 474 | pathology-confirmed (CIR IDs) |
| **LUNGx / SPIE-AAPM-NCI** | TCIA + xlsx | 74 | 91 | 1:1 size-matched benign/malignant |
| **CIRDataset** (Zenodo 6762573) | Choi/Dahiya/Nadeem | 883 LIDC + 83 LUNGx | 966 | radiologist QA/QC'd paper-grade NRRD masks |

### Choi 2018 Med Phys + Choi 2021 CMPB — detailed breakdown

LIDC-IDRI malignancy ≥4 vs ≤2 binary classification. 5-fold patient-grouped CV.

| Method | Features | n (RM) | RM AUC | PM AUC (XML mask) | PM AUC (CIR mask) |
|---|--:|--:|---|---|---|
| `radiomics50` (Med Phys 2018) | 1,409 → top-50 | 4,248 | **0.872 ± 0.010** | 0.748 ± 0.046 | **0.868 ± 0.039** |
| `spic6` (CMPB 2021) | 6 | 4,248 | **0.816 ± 0.006** | 0.715 ± 0.059 | 0.831 ± 0.084 |
| `cmpb2021_size+spic` | 7 | 4,248 | 0.832 ± 0.021 | 0.727 ± 0.059 | 0.865 ± 0.051 |
| `radiomics+spic` (union, top-50) | 1,415 → top-50 | 4,248 | 0.867 ± 0.024 | 0.755 ± 0.046 | **0.868 ± 0.039** |

`spic6` reproduces CMPB 2021 with very tight CI (0.816 ± 0.006 — paper midpoint, CI excludes both 0.80 and 0.83). With CIR paper-grade masks the LIDC-PM PM AUC reaches **0.868**, exceeding the paper's reported 0.85.

### Choi 2022 MICCAI / CIR — LUNGx external validation

Train on LIDC RM (≥4 vs ≤2), domain-adapt on the LUNGx 10-patient CalibrationSet, test on the LUNGx 60-patient TestSet.

| Method | n train / cal / test | AUC (no cal) | **AUC (ext + cal)** |
|---|---|---|---|
| `radiomics50` (CIR mask) | 4,248 / 10 / 73 | 0.725 | **0.756** |
| `radiomics+spic` (CIR mask) | 4,248 / 10 / 73 | 0.725 | **0.756** |
| `spic6` (CIR mask) | 4,248 / 10 / 73 | 0.713 | 0.713 |
| `size_only` (sanity) | 4,248 / 10 / 73 | ≤0.5 | ≤0.5 |

This exactly matches the CMPB 2021 LUNGx external number (paper: 0.76) — reproduced using interpretable features only (no neural-network encoder). Note: LUNGx is 1:1 benign/malignant size-matched by design, nullifying size as a predictor and creating a large LIDC→LUNGx distribution shift. Without the 10-patient calibration step, `radiomics50` drops to 0.725.

### LCSR port-vs-reference validation (shape module)

`qradiomics.shape.spiculation_from_voxel` vs LCSR reference on the same CIRDataset input masks:

| Cohort | n | Spearman ρ (qr_Na × lcsr_Na) | Spearman ρ (qr_Nl × lcsr_Nl) |
|---|--:|---|---|
| LIDC | 883 | **0.459** (p = 4×10⁻⁴⁷) | 0.349 (p = 1×10⁻²⁶) |
| LUNGx | 83 | **0.653** (p = 2×10⁻¹¹) | 0.370 (p = 6×10⁻⁴) |

For context, Choi 2021 reports ρ = 0.44 between spiculation count and radiologist spiculation score — our port-vs-LCSR ρ is in the same range. The qradiomics port runs in seconds per nodule (vs minutes for LCSR's full cMCF+OMT C++ pipeline), making 1,018-patient cohort runs feasible on a single workstation.

### Methods harness

`pipelines/lidc_idri/methods_compare.py` is a drop-in benchmark harness. Any feature-extraction method that produces a wide features CSV plugs in via a single line:

```python
METHODS["my_method"] = lambda df: [c for c in df.columns if c.startswith("my_prefix_")]
```

The same RM / PM / LUNGx-cal / LUNGx-test splits and leakage-safe RF CV are applied automatically. Built-in methods: `aerts4`, `radiomics50`, `spic6`, `cmpb2021_size+spic`, `radiomics+spic`, `shape_only`, `firstorder`, `size_only`.

## Validated Cohorts

| Cohort | Format on TCIA | Conversion path |
|---|---|---|
| [NSCLC-Radiomics (LUNG1)](https://www.cancerimagingarchive.net/collection/nsclc-radiomics/) | DICOM CT + RTSTRUCT | `qr convert dicom-series` + `qr convert rtstruct --roi GTV-1` |
| [NSCLC-Cetuximab](https://www.cancerimagingarchive.net/collection/nsclc-cetuximab/) | DICOM CT + RTSTRUCT | `qr convert dicom-series` + `qr convert rtstruct --roi PTV` |
| [ACRIN-NSCLC-FDG-PET](https://www.cancerimagingarchive.net/collection/acrin-nsclc-fdg-pet/) | DICOM CT/PET + RTSTRUCT | `qr convert dicom-series` + `qr convert rtstruct --roi Heart` |

## Command Reference

| Command | Stage | Purpose |
|---|---|---|
| `qr tcia download` | data | Bulk-download a TCIA collection (multi-process + progress) |
| `qr anonymize` | data | Strip PHI from a DICOM tree (DICOM PS3.15 Annex E) |
| `qr convert dicom-series` | data/image | DICOM CT/MR → NRRD; PT auto-routes through SUV conversion |
| `qr convert rtstruct` | data/image | DICOM RTSTRUCT contour → label NRRD (case-insensitive ROI) |
| `qr convert manifest-from-dir` | data | Glob image+mask pairs into a manifest CSV |
| `qr extract` | features | PyRadiomics → `features.csv` (manifest + pattern) |
| `qr results merge` | features | `features.csv` + `clinical.csv` → `analysis_ready.csv` |
| `qr analyze survival` | modeling | Univariate Cox proportional hazards |
| `qr analyze classify` | modeling | Univariate logistic regression |
| `qr analyze importance` | modeling | Random-forest + permutation (+ optional SHAP) |
| `qr ml train` | modeling | CV Cox / logistic + leakage-safe corr/univariate selection |
| `qr ml predict` | modeling | Apply a trained model to new features |
| `qr ml evaluate` | modeling | Hold-out evaluation report (c-index / AUC) |
| `qr workflow plan` | assembly | Generate a multi-step plan from a template |
| `qr workflow show` | assembly | Inspect a plan's steps and variables |
| `qr workflow scaffold` | assembly | Render a plan as shell / nextflow / prefect |
| `qr workflow run` | assembly | Execute a plan (default executor: nextflow) |
| `qr pattern list` / `search` | meta | Browse bundled pattern templates |
| `qr config get` / `set` | meta | User preferences in `~/.qradiomics/config.yaml` |

## Python API — atomic core

Every CLI command is a thin wrapper around a re-usable Python API. External libraries (e.g. longitudinal CBCT orchestrators) consume the atomic layer directly instead of shelling out.

```python
from qradiomics.atomic import (
    load_image_and_mask, preprocess_pair,
    build_extractor, run_extractor, extract_features,
    register_pair, resample_to_fixed, histogram_match_hu,
)
from qradiomics.data_model import (
    Cohort, Patient, TreatmentCourse, Study,
    ImageSeries, RTStructureSet, ROI,
    AtomicUnit, Modality, StudyType,
    save_cohort, load_cohort,
)
from qradiomics.manifest import flatten_cohort, read_manifest, write_manifest
from qradiomics.delta import DeltaPair, compute_delta, compute_trend
from qradiomics.io.dicom import read_pet_suv

# Single atomic unit: one image, one mask → ≈1409 features
image, mask = load_image_and_mask("planCT.nrrd", "Heart-label.nrrd")
cropped_img, cropped_msk = preprocess_pair(image, mask, pad_mm=20, resample_mm=1.0)
extractor = build_extractor(image_types=["Original", "LoG", "Wavelet"])
features = run_extractor(extractor, cropped_img, cropped_msk)
```

### Hierarchical cohort model

`qradiomics.data_model` mirrors the canonical 5–6 level hierarchy used across the Choi-Lab ecosystem:

```
Cohort → Patient → TreatmentCourse → Study → ImageSeries / RTStructureSet → ROI
                       (optional)
```

Diagnostic-only cohorts omit `TreatmentCourse` and attach `Study` directly to `Patient`. `flatten_cohort()` walks the tree and produces a list of `AtomicUnit`s — one per (image, mask) pair — which becomes the manifest CSV consumed by `qr extract`.

```python
cohort = Cohort(cohort_id="lng-cbct")
patient = Patient(patient_id="P001")
course = TreatmentCourse(course_id="rt1", fractions=30, prescription_dose_gy=60.0)
study = Study(study_id="S-week4", timepoint="week4", relative_day=28)
study.series["CBCT"] = ImageSeries(series_id="CBCT-w4",
    image_path="/data/CBCT_w4.nrrd", modality=Modality.CBCT, image_tag="CBCT-w4")
rs = RTStructureSet(rtstruct_id="rs", referenced_series_uid="...")
rs.rois["GTV"] = ROI(roi_id="GTV", mask_path="/data/GTV-label.nrrd",
                     mask_tag="manual", mask_image_tag="CBCT-w4")
study.structure_sets["rs"] = rs
course.studies[study.study_id] = study
patient.treatment_courses[course.course_id] = course
cohort.patients[patient.patient_id] = patient

units = flatten_cohort(cohort)         # list[AtomicUnit]
write_manifest(units, "manifest.csv")  # canonical 10-column schema
save_cohort(cohort, "cohort.yaml")     # full graph persistence
```

## Shape Analysis — `qradiomics.shape`

Python re-implementations of two published Choi-Lab pipelines, used as a library (no CLI yet — call as functions):

**2014 CMPB — AHSN pulmonary nodule detection**

```python
from qradiomics.shape import (
    surface_elements,          # Hessian eigendecomp + per-voxel normals (§2.2.1)
    detect_candidates,         # Multi-scale Sato/Li dot enhancement (§2.2.2)
    ahsn, AHSNConfig,          # Angular Histogram of Surface Normals (§2.3.1)
    wall_eliminate,            # Iterative wall detection / elimination (§2.3.2)
    make, make_all,            # Synthetic 3D lung phantoms for testing
)
```

**2021 CMPB — Spiculation quantification** (companion to [CIR](https://github.com/choilab-jefferson/CIR))

```python
from qradiomics.shape import (
    voxel_to_mesh,                  # marching cubes → triangular mesh
    spherical_parameterization,     # cotangent-Laplacian → unit sphere
    area_distortion,                # per-vertex log-area distortion
    detect_peaks,                   # negative-distortion peaks = spike candidates
    spiculation_features,           # Na / Nl / Na_att / s1 / s2 features
    spiculation_from_voxel,         # one-shot mask → SpiculationFeatures
)
```

See `tests/shape/` for end-to-end usage on analytic shapes (sphere / spiked-sphere / phantoms).

## Repository Layout

```
qradiomics/
├── __init__.py              # exposes PatternLoader, RadiomicsExtractor, __version__
├── cli/                     # Click CLI (qr / qradiomics / qrdx)
│   ├── main.py
│   ├── config_io.py
│   ├── commands/            # extract, results, analyze, config_cmd
│   └── pattern/             # list, match
├── atomic.py                # load_image_and_mask, preprocess_pair, build/run_extractor
├── data_model.py            # Cohort → Patient → TreatmentCourse → Study → Series → ROI
├── manifest.py              # flatten_cohort, read/write_manifest
├── delta.py                 # DeltaPair, compute_delta, compute_trend
├── io/dicom.py              # read_pet_suv
├── pattern_loader.py        # YAML pattern templates → Pydantic models
├── extractor.py             # PyRadiomics wrapper
├── shape/                   # Published shape pipelines (re-implementation)
│   ├── hessian.py           # 2014 §2.2.1 — Hessian + surface elements
│   ├── detection.py         # 2014 §2.2.2 — multi-scale Sato/Li dot filter
│   ├── ahsn.py              # 2014 §2.3.1 — AHSN descriptor
│   ├── wall_elim.py         # 2014 §2.3.2 — iterative wall elimination
│   ├── mesh_utils.py        # 2021 — voxel → mesh + geometry primitives
│   ├── spiculation.py       # 2021 — spherical param + Na/Nl/Na_att/s1/s2
│   └── phantoms.py          # Synthetic 3D lung phantoms for testing
└── data/
    ├── templates/           # pattern YAMLs (ct_default, nsclc_survival, ...)
    ├── pyradiomics/         # per-pattern PyRadiomics extractor configs
    └── schema/              # pattern-template JSON schema

tests/                       # pytest: analyze + results.merge (19 tests)
LICENSE                      # MIT
pyproject.toml
```

## Bundled Pattern Templates

| `pattern_id` | Description |
|---|---|
| `ct-default` | Plain CT, single timepoint, multi image-type baseline |
| `standard-radiomics` | Multi-modality generic radiomics |
| `survival-analysis` | Cox + RSF + KM, time-to-event task |
| `nsclc-survival` | NSCLC CT GTV, LoG+Wavelet+Square/Sqrt/Log image types |

Drop a new `*.yaml` into `qradiomics/data/templates/` to add a study; `qr pattern list` picks it up automatically.

## Citing

If you use this CLI in published work, please cite the relevant upstream papers. PyRadiomics and the NSCLC-Radiomics cohort are the two essential citations for any qradiomics-derived feature analysis:

- **PyRadiomics** — van Griethuysen JJM, Fedorov A, Parmar C, et al. *Computational Radiomics System to Decode the Radiographic Phenotype.* Cancer Research 2017; 77(21):e104-e107. [doi:10.1158/0008-5472.CAN-17-0339](https://doi.org/10.1158/0008-5472.CAN-17-0339)
- **NSCLC-Radiomics (TCIA LUNG1)** — Aerts HJWL, Velazquez ER, Leijenaar RTH, et al. *Decoding tumour phenotype by noninvasive imaging using a quantitative radiomics approach.* Nature Communications 2014; 5:4006. [doi:10.1038/ncomms5006](https://doi.org/10.1038/ncomms5006)

If you build on the lung-screening lineage that this CLI grew out of, please additionally cite:

- Choi W, Oh JH, Riyahi S, Liu C-J, Jiang F, Chen W, White C, Rimner A, Mechalakos JG, Deasy JO, Lu W. *Radiomics analysis of pulmonary nodules in low-dose CT for early detection of lung cancer.* Medical Physics 2018; 45(4):1537-1549. [doi:10.1002/mp.12820](https://doi.org/10.1002/mp.12820)
- Choi W, Nadeem S, Riyahi S, Deasy JO, Tannenbaum A, Lu W. *Reproducible and Interpretable Spiculation Quantification for Lung Cancer Screening.* Computer Methods and Programs in Biomedicine 2021; 200:105839. [doi:10.1016/j.cmpb.2020.105839](https://doi.org/10.1016/j.cmpb.2020.105839)
- Choi WJ, Choi TS. *Automated pulmonary nodule detection based on three-dimensional shape-based feature descriptor.* Computer Methods and Programs in Biomedicine 2014; 113(1):37-54. [doi:10.1016/j.cmpb.2013.08.015](https://doi.org/10.1016/j.cmpb.2013.08.015)

## Authors and Acknowledgements

- [**Wookjin Choi**](https://github.com/taznux) — overall architecture, CLI design, pattern templates
- [**Pradeep Bhetwal**](https://github.com/Pradeepbhetwal) — survival analysis on the LUNG1 cohort
- *Choi Lab, Department of Radiation Oncology, Sidney Kimmel Medical College at Thomas Jefferson University*

## License

MIT — see [LICENSE](https://github.com/choilab-jefferson/qradiomics/blob/main/LICENSE).
