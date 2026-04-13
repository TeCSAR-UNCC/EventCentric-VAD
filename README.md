# EventCentric-VAD
This repoitory includes the code for the paper [From Frames to Events: Rethinking Evaluation in Human-Centric Video Anomaly Detection](https://arxiv.org/pdf/2604.09327), accepted for CVPR 2026 conference. In this work, we challenge the conventional frame-level evaluation paradigm in video anomaly detection (VAD), showing that it fails to capture the temporal nature of real-world anomalies and often overestimates model performance.

We propose an event-centric framework that focuses on detecting coherent anomalous events with meaningful start and end boundaries. To achieve this, we introduce (1) a score-refinement pipeline that transforms noisy frame-level predictions into temporally consistent events, and (2) a dual-branch reconstruction model that directly produces event-level anomaly scores using multi-scale temporal context.

We also establish a new evaluation protocol based on temporal IoU and event-level F1 metrics, revealing a significant gap between frame-level accuracy and true event-level performance across standard VAD benchmarks
