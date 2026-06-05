---
title: "PathCNN: interpretable convolutional neural networks for survival prediction and pathway analysis applied to glioblastoma"
date: "2021-07-22T12:57:18.000-04:00"
categories: 
  - "paper"
  - "research"
tags: 
  - "cancer"
  - "cnn"
  - "deep-learning"
  - "glioblastoma"
  - "image"
  - "pathcnn"
  - "pathway"
  - "survival"
aliases:
  - /2021/07/22/pathcnn-interpretable-convolutional-neural-networks-for-survival-prediction-and-pathway-analysis-applied-to-glioblastoma/
description: "Jung Hun Oh, Wookjin Choi, Euiseong Ko, Mingon Kang, Allen Tannenbaum, Joseph O Deasy The authors wish it to be known that, in their opinion, Jung Hun Oh..."
---

Jung Hun Oh, Wookjin Choi, Euiseong Ko, Mingon Kang, Allen Tannenbaum, Joseph O Deasy

The authors wish it to be known that, in their opinion, Jung Hun Oh and Wookjin Choi should be regarded as Joint First Authors.

[https://academic.oup.com/bioinformatics/article/37/Supplement\_1/i443/6319702](https://academic.oup.com/bioinformatics/article/37/Supplement_1/i443/6319702)

<figure>

https://github.com/mskspi/PathCNN/raw/main/img/pathcnn.png

<figcaption>

An illustration of biological interpretation. (**A**) Grad-CAM procedure to generate class activation maps. The two images on the left bottom represent an example of the class activation maps for a sample in the cohort, which were generated from Grad-CAM procedure; (**B**) statistical analysis to identify significantly different pathways between the LTS and non-LTS groups. LTS, long-term survival; CNN, convolutional neural network; ReLU, rectified linear unit

</figcaption>

</figure>

## Abstract

Motivation

Convolutional neural networks (CNNs) have achieved great success in the areas of image processing and computer vision, handling grid-structured inputs and efficiently capturing local dependencies through multiple levels of abstraction. However, a lack of interpretability remains a key barrier to the adoption of deep neural networks, particularly in predictive modeling of disease outcomes. Moreover, because biological array data are generally represented in a non-grid structured format, CNNs cannot be applied directly.

Results

To address these issues, we propose a novel method, called _PathCNN_, that constructs an interpretable CNN model on integrated multi-omics data using a newly defined _pathway image_. PathCNN showed promising predictive performance in differentiating between long-term survival (LTS) and non-LTS when applied to glioblastoma multiforme (GBM). The adoption of a visualization tool coupled with statistical analysis enabled the identification of plausible pathways associated with survival in GBM. In summary, PathCNN demonstrates that CNNs can be effectively applied to multi-omics data in an interpretable manner, resulting in promising predictive power while identifying key biological correlates of disease.Availability and implementation

The source code is freely available at: [https://github.com/mskspi/PathCNN](https://github.com/mskspi/PathCNN).

https://www.youtube.com/watch?v=K0cuEp1ID0o
