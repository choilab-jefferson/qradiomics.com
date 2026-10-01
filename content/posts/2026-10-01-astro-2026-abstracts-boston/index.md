---
title: "Six Abstracts at ASTRO 2026"
date: "2026-10-01T09:00:00.000-04:00"
categories:
  - "news"
  - "research"
tags:
  - "ASTRO"
  - "ASTRO2026"
  - "CBCT"
  - "Radiomics"
  - "LLM"
  - "EHR"
  - "Cardio-Oncology"
  - "Plan Quality"
  - "MR-guided Radiotherapy"
  - "PET/CT"
aliases:
  - /2026/10/01/astro-2026-abstracts-boston/
description: "Six abstracts from our collaborations appear in the ASTRO 2026 supplement of the Red Journal: longitudinal CBCT survival prediction, PET radiomics for cardiac risk, plan quality scoring, LLM-based EHR extraction, MR-guided tumor tracking, and bone metastasis case-finding."
---

Six abstracts from our collaborations appear in the ASTRO 2026 Annual Meeting supplement of *IJROBP* 126(1), published September 1, 2026. Three are oral-type presentations (one *BEST of Physics* oral, one oral, one Quick Pitch oral) and one is a poster. The format of the other two is not stated here. The lead abstract also received an ASTRO abstract award ([details]({{< relref "/posts/2026-07-27-2026-astro-annual-meeting-abstract-award" >}})).

## Overview

| Choi's role | Abstract | Presenter | Format | Date and time (ET) |
|---|---|---|---|---|
| PI | Longitudinal CBCT survival prediction | Wookjin Choi, PhD | *BEST of Physics* oral | Sep 28, 11:05-11:15 |
| Senior author | PET radiomics cardiac risk | Devanshu Panchal, PhD | Quick Pitch oral | Sep 30, 09:15-09:20 |
| Senior author | Minimum cohort size for plan scoring | Cella Kove, BA | Poster | Sep 28, 10:45-12:00 |
| Data and infrastructure | MR-guided tumor tracking | Swati Rampalli, BS | not stated | not stated |
| Data and infrastructure | LLM triage of bone metastases | Robert Walker, MD, MS | not stated | not stated |
| Co-author | TRACER cardiac event extraction | Wenchao Cao, PhD | Oral | Sep 28, 08:40-08:50 |

## Led by our lab

**Early adaptive interventions in lung cancer** (presenter: Wookjin Choi; PI). See the [acceptance post]({{< relref "/posts/2026-05-18-astro-2026-best-of-physics-oral-acceptance" >}}) and the earlier [longitudinal CBCT radiomics work]({{< relref "/posts/2023-02-10-longitudinal-cbct-radiomics-in-lung-cancer-supported-by-varian-medical-systems-inc" >}}). [IJROBP 126(1) S91](https://doi.org/10.1016/j.ijrobp.2026.06.112). The study used 225 courses from 189 patients (5,067 CBCTs, 2019-2024, single institution), with 107 radiomic features per GTV/PTV contour and 14 clinical variables. A hierarchical gradient boosting survival model aggregates lesions to the patient level, then integrates cumulatively over time (CBCTcN is fraction 1 through week N), evaluated with 5-fold patient-level cross-validation. The cumulative model peaked by week 2 (CBCTc2 C-index 0.72, CV 6.12%). The six-week model reached a C-index of 0.72 (95% CI 0.69-0.75), and its CV fell from 8.47% at week 1 to 1.97% at week 6. It outperformed clinical-only (0.61, p<0.001), planning CT radiomics (0.66, p=0.015), and delta-radiomics (0.70, p=0.006). Adding clinical variables did not significantly improve discrimination despite the word "fusion" in the title. The abstract concludes that prognostic accuracy is strong by week 2, later weeks stabilize predictions, and the approach uses standard-of-care imaging.

## Senior author

**Clinical and PET radiomics for pre-therapy cardiac risk** (presenter: Devanshu Panchal). Earlier cardiac PET work: [functional radiomics]({{< relref "/posts/2023-09-11-novel-functional-delta-radiomics-for-predicting-overall-survival-in-lung-cancer-radiotherapy-using-cardiac-fdg-pet-uptake" >}}) and [cardiac risks with PET]({{< relref "/posts/2024-04-14-shining-a-light-unveiling-cardiac-risks-using-pet-imaging-in-lung-cancer-radiotherapy" >}}). [IJROBP 126(1) S296](https://doi.org/10.1016/j.ijrobp.2026.06.624). Two retrospective cohorts with strict train-test separation: cohort A (SBRT, n=95, 48% cardiac events) for development and cohort B (mixed fractionation, n=89, 24% events) as an independent test. Clinical-only, radiomics-only, and mid-fusion models were compared, with ExtraTrees performing best. Test AUC/AP was 0.550/0.255 for clinical, 0.663/0.398 for radiomics, and 0.666/0.485 for mid-fusion. The AUC gain of fusion over radiomics alone is small, while the AP gain is larger.

**How many plans are enough?** (presenter: Cella Kove). [IJROBP 126(1) e231-e232](https://doi.org/10.1016/j.ijrobp.2026.06.1163). Using 238 prostate VMAT plans (70 Gy in 28 fractions, 2022-2026), a DVH z-score composite was converted to a percentile, and 800 bootstraps were run over N=10-230. CI width plateau and KS distance both stabilized near N=200 (CI width 1.237 at N=50 and 0.599 at N=200). This holds for this prostate protocol and scoring framework; other sites need the same check.

## Data collection and computational infrastructure

**Computer vision tracking for MR-guided radiotherapy** (presenter: Swati Rampalli). Related: [MR-guided adaptive radiotherapy segmentation]({{< relref "/posts/2023-10-07-deep-learning-segmentation-for-accurate-gtv-and-oar-segmentation-in-mr-guided-adaptive-radiotherapy-for-pancreatic-cancer-patients" >}}). [IJROBP 126(1) e265](https://doi.org/10.1016/j.ijrobp.2026.06.1239). SiamMask and XMem were compared on 50 TrackRad2025 patients (25 at 0.35T, 25 at 1.5T) without medical retraining. XMem reached a DSC of 0.861 +/- 0.168 versus 0.773 +/- 0.232, and an HD95 of 5.51 versus 9.62 mm. Both models did worse at 0.35T. The abstract cautions that DSC and IoU alone do not establish clinical viability.

**AI language model for high-risk asymptomatic bone metastases on PET/CT** (presenter: Robert Walker). [IJROBP 126(1) e412](https://doi.org/10.1016/j.ijrobp.2026.06.1563). Among 93 Stage IV patients, 19 (20%) were high-risk. Six local LLMs (4-120B parameters) were evaluated against expert review. The best accuracy was 92.8% (sensitivity 88.2%, specificity 96.3%), and three models reached 100% sensitivity with specificity of 85-88%. PPV ranged from 37% to 75%. This is an evaluation of high-sensitivity case-finding and triage, not automated referral.

## Co-author

**TRACER** (presenter: Wenchao Cao). *Cross-Institutional Validation of LLM-Based Cardiac Event Extraction from Electronic Health Records.* See the [TRACER post]({{< relref "/posts/2026-07-01-tracer-open-source-llms-cardiac-event-extraction" >}}) for details, the [Jefferson Investigates coverage]({{< relref "/posts/2026-08-31-jefferson-investigates-features-tracer" >}}), and the [journal article](https://www.sciencedirect.com/science/article/pii/S0360301626039131) ([DOI](https://doi.org/10.1016/j.ijrobp.2026.06.3060)).

## Related posts

- [Selected for ASTRO 2026 BEST of Physics]({{< relref "/posts/2026-05-18-astro-2026-best-of-physics-oral-acceptance" >}}): acceptance of the lead abstract.
- [ASTRO 2026 abstract award]({{< relref "/posts/2026-07-27-2026-astro-annual-meeting-abstract-award" >}}): the award for the lead abstract.
- [Longitudinal CBCT radiomics supported by Varian]({{< relref "/posts/2023-02-10-longitudinal-cbct-radiomics-in-lung-cancer-supported-by-varian-medical-systems-inc" >}}): earlier funding for the CBCT work.
- [Functional radiomics for cardiotoxicity]({{< relref "/posts/2023-09-11-novel-functional-delta-radiomics-for-predicting-overall-survival-in-lung-cancer-radiotherapy-using-cardiac-fdg-pet-uptake" >}}): cardiac FDG-PET uptake in lung cancer radiotherapy.
- [Cardiac risks using PET imaging]({{< relref "/posts/2024-04-14-shining-a-light-unveiling-cardiac-risks-using-pet-imaging-in-lung-cancer-radiotherapy" >}}): cardiac PET study overview.
- [The Nexus featured our cardiac PET radiomics study]({{< relref "/posts/2024-06-27-the-nexus-featured-our-cardiac-pet-radiomics-study" >}}): media coverage of that study.
- [TRACER]({{< relref "/posts/2026-07-01-tracer-open-source-llms-cardiac-event-extraction" >}}): open-source LLM cardiac event extraction.
- [Jefferson Investigates features TRACER]({{< relref "/posts/2026-08-31-jefferson-investigates-features-tracer" >}}): media coverage of TRACER.
- [MR-guided adaptive radiotherapy segmentation]({{< relref "/posts/2023-10-07-deep-learning-segmentation-for-accurate-gtv-and-oar-segmentation-in-mr-guided-adaptive-radiotherapy-for-pancreatic-cancer-patients" >}}): earlier MR-guided work.
- [8 abstracts accepted for AAPM 2026]({{< relref "/posts/2026-07-06-8-abstracts-accepted-aapm-2026" >}}): the group's other 2026 meeting abstracts.

## Common thread

Across these abstracts, the aim is to turn repeated or heterogeneous clinical observations (serial CBCTs, EHR text, PET scans, treatment plans, MR cine images) into stable decision information.

Thank you to the presenters and to every collaborator who contributed to this work.
