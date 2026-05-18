---
title: "qradiomics — Serverless Radiomics Research CLI"
date: "2026-05-17T20:31:21.000-04:00"
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
---

**License:** MIT · **Python:** 3.11+ · **Repo:** [choilab-jefferson/qradiomics](https://github.com/choilab-jefferson/qradiomics)

Serverless radiomics research CLI. `qr` does two things equally well:

- **Atomic tasks** — convert DICOM, extract features, merge clinical, fit a model. Each is a single command, files in / files out.
- **Workflow assembly** — generate, mutate, scaffold, and run multi-step pipelines from those atomic tasks. Default executor is **Nextflow** (per-patient parallel + cache + HPC); **Prefect** is the secondary executor; **inline** is the small-cohort fallback.

The canonical radiomics data flow has four stages — **data → image → features → modeling** — and one `qr workflow plan` call instantiates the whole chain:

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

## Background — three earlier projects, unified

`qradiomics` is the modern Python successor of three earlier Choi Lab radiomics codebases. The MATLAB pipelines, the ITK / Ruffus C++ tools, and the Docker-based screening workflow are distilled here into a single Click CLI built on PyRadiomics, scikit-learn, and lifelines:

| Earlier project | Stack | Role | This repo |
|---|---|---|---|
| [taznux/lung-image-analysis](https://github.com/taznux/lung-image-analysis) | MATLAB · MIT | LIDC-IDRI nodule detection / segmentation / characterization | superseded |
| [taznux/radiomics-tools](https://github.com/taznux/radiomics-tools) | C++/Python (ITK, Ruffus) · MIT | DICOM tools, GrowCut segmentation, feature extraction pipeline | superseded |
| [choilab-jefferson/LungCancerScreeningRadiomics](https://github.com/choilab-jefferson/LungCancerScreeningRadiomics) | MATLAB / Python · GPL-3.0 | LIDC + LUNGx end-to-end screening workflow with AutoML | superseded (this repo re-implements the open subset under MIT using PyRadiomics) |

The AHSN shape descriptor pipeline (CMPB 2014) and the spiculation quantification pipeline (CMPB 2021, companion to [choilab-jefferson/CIR](https://github.com/choilab-jefferson/CIR)) are re-integrated in `qradiomics.shape` (see Shape Analysis below). The longitudinal CBCT / delta-radiomics workflows (ASTRO / AAPM 2026) will be released here after publication.

## Install

```bash
pip install -e .            # core CLI + library
pip install -e .[rtstruct]  # plus rt-utils for `qr convert rtstruct`
```

Python 3.11 or newer is required. PyRadiomics, SimpleITK, lifelines, scikit-learn, statsmodels, scipy, and pandas are pulled in as dependencies.

After install, `qr`, `qradiomics`, and `qrdx` are available on `$PATH` and point at `qradiomics.cli.main:cli`.

## DICOM Conversion

Many TCIA cohorts ship as DICOM (CT/PET/MR series + RTSTRUCT). Two helpers convert into the NRRD form the rest of the pipeline consumes:

```bash
# 1. CT/PET/MR DICOM series → single NRRD volume
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

RTSTRUCT conversion uses `rt-utils` (install via `pip install qradiomics[rtstruct]`). ROI lookup is case-insensitive (a `--roi Heart` request matches a structure set with `heart`). The mask is auto-reshaped to the CT geometry, with a ±1-slice z-axis trim/pad when the structure set references slices outside the series.

## End-to-end Example

Once you have a manifest CSV (canonical lowercase columns: `patient_id, modality, image_path, mask_path`):

```bash
# 1. Extract features under a bundled pattern
#    nsclc-survival → Original + LoG + Wavelet + Square + SquareRoot + Logarithm
#                     × {firstorder, shape, glcm, glrlm, glszm, gldm, ngtdm}
qr extract -m manifest.csv -p nsclc-survival -o features.csv
# -> ~1130 features per patient with nsclc-survival
# -> ~1409 features per patient with ct-default (includes LBP/Exponential/Gradient)

# 2. Join with the clinical CSV on patient_id
#    Auto-detects days vs months (median > 100 → divides by 30.44 → OS_months)
qr results merge \
  -f features.csv -c clinical.csv \
  --clinical-id-col patient_id \
  --time-col OS_days --event-col OS_event \
  -o analysis_ready.csv

# 3. Univariate Cox PH on every radiomic feature
qr analyze survival -i analysis_ready.csv \
  --outcome OS_months --event OS_event \
  -o cox_results.csv
```

Browse the bundled patterns with `qr pattern list` and `qr pattern search <kw>`.

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

## Workflow Assembly — agents compose, qr executes

The canonical four-stage data flow is encoded in the template library that `qr workflow plan` draws from:

| Template | Stages covered | When to use |
|---|---|---|
| `nrrd_survival` | data → features → modeling | cohort already in NRRD form |
| `dicom_survival` | data → image → features → modeling | cohort ships as DICOM + RTSTRUCT |
| `dicom_to_ml` | data → image → features → modeling (ML) | full end-to-end DICOM → trained model + CV metrics + held-out evaluation |

```bash
# 1. Generate a plan
qr workflow plan -t dicom_to_ml \
    -d /data/cohort -c clinical.csv \
    --roi GTV --pattern nsclc-survival \
    -o plan.json

# 2. (Optional) scaffold a Nextflow file for inspection / editing
qr workflow scaffold -p plan.json -e nextflow -o pipeline.nf

# 3. Run — default executor is Nextflow (per-patient parallel + cache)
qr workflow run plan.json
qr workflow run plan.json --executor inline      # small interactive
qr workflow run plan.json --executor prefect     # Prefect-orchestrated
```

The plan is plain JSON/YAML — agents can read, mutate (add a stage, swap a pattern, change the executor), and re-run without re-templating. Per-patient steps are marked in the plan and fanned out automatically by the Nextflow / Prefect scaffolders.

## Validated Cohorts

The pipeline has been validated end-to-end on three TCIA public cohorts:

| Cohort | Format on TCIA | Conversion path |
|---|---|---|
| **NSCLC-Radiomics (LUNG1)** | DICOM CT + RTSTRUCT (or pre-converted NRRD via the published companion pack) | `qr convert dicom-series` + `qr convert rtstruct --roi GTV-1`, or feed NRRD directly |
| **NSCLC-Cetuximab** | DICOM CT + RTSTRUCT | `qr convert dicom-series` + `qr convert rtstruct --roi PTV` |
| **ACRIN-NSCLC-FDG-PET** | DICOM CT/PET + RTSTRUCT | `qr convert dicom-series` + `qr convert rtstruct --roi Heart` (case-insensitive) |

All three flow cleanly through `convert → extract → results merge → analyze`. Ready-to-run shell scripts for each cohort (plus LIDC-IDRI and the IBSI phantom) live in `examples/`.

## Command Reference

| Command | Stage | Purpose |
|---|---|---|
| `qr convert dicom-series` | data/image | DICOM CT/PET/MR series → NRRD |
| `qr convert rtstruct` | data/image | DICOM RTSTRUCT contour → label NRRD (case-insensitive ROI) |
| `qr convert manifest-from-dir` | data | Glob image+mask pairs into a manifest CSV |
| `qr extract` | features | PyRadiomics → `features.csv` (manifest + pattern) |
| `qr results merge` | features | `features.csv` + `clinical.csv` → `analysis_ready.csv` |
| `qr analyze survival` | modeling | Univariate Cox proportional hazards |
| `qr analyze classify` | modeling | Univariate logistic regression |
| `qr analyze importance` | modeling | Random-forest + permutation (+ optional SHAP) |
| `qr ml train` | modeling | k-fold CV Cox / logistic model → `model.pkl` + `metrics.json` |
| `qr ml predict` | modeling | Apply a trained model to new features |
| `qr ml evaluate` | modeling | Hold-out evaluation report (c-index / AUC) |
| `qr workflow plan` | assembly | Generate a multi-step plan from a template |
| `qr workflow show` | assembly | Inspect a plan's steps and variables |
| `qr workflow scaffold` | assembly | Render a plan as shell / nextflow / prefect |
| `qr workflow run` | assembly | Execute a plan (default executor: nextflow) |
| `qr pattern list` / `search` | meta | Browse bundled pattern templates |
| `qr config get` / `set` | meta | User preferences in `~/.qradiomics/config.yaml` |

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

**2021 CMPB — Spiculation quantification (companion to CIR)**

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

- **Wookjin Choi** — overall architecture, CLI design, pattern templates
- **Pradeep Bhetwal** — survival analysis on the LUNG1 cohort
- *Choi Lab, Department of Radiation Oncology, Sidney Kimmel Medical College at Thomas Jefferson University*

## License

MIT — see [LICENSE](https://github.com/choilab-jefferson/qradiomics/blob/main/LICENSE).
