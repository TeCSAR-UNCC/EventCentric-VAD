# EventCentric-VAD
This repoitory includes the code for the paper [From Frames to Events: Rethinking Evaluation in Human-Centric Video Anomaly Detection](https://arxiv.org/pdf/2604.09327), accepted for CVPR 2026 conference. In this work, we challenge the conventional frame-level evaluation paradigm in video anomaly detection (VAD), showing that it fails to capture the temporal nature of real-world anomalies and often overestimates model performance.

We propose an event-centric framework that focuses on detecting coherent anomalous events with meaningful start and end boundaries. To achieve this, we introduce (1) a score-refinement pipeline that transforms noisy frame-level predictions into temporally consistent events, and (2) a dual-branch reconstruction model that directly produces event-level anomaly scores using multi-scale temporal context.

We also establish a new evaluation protocol based on temporal IoU and event-level F1 metrics, revealing a significant gap between frame-level accuracy and true event-level performance across standard VAD benchmarks

###Event-centric Characterization of VAD benchmarks
We establish a foundation by auditing existing VAD datasets, SHT [19], CHAD [6], HuVAD [25], and NWPUC [4], from an event-centric perspective.

<sub> Table: Frame-level and event-level statistics of VAD benchmarks.
| Granularity | Characteristic      | SHT     | CHAD   | HuVAD   | NWPUC  |
|------------|--------------------|---------|--------|---------|--------|
| Frame      | Normal Frames      | 24,077  | 67,303 | 694,415 | 318,793 |
|            | Anomalous Frames   | 16,714  | 59,172 | 225,075 | 65,266  |
| Event      | Anomalous Events   | 121     | 190    | 1,691   | 137     |
|            | Avg. Duration (f)  | 138.13  | 311.43 | 133.10  | 476.39  |

Our event-centric analysis shows that the widely used SHT dataset contains micro-events, which are anomalous sequences spanning only a few frames. These likely represent manual annotation noise rather than semantically meaningful human actions. We audited the SHT test set by cross-referencing binary masks with the original videos, filtering out these physically impossible events to ensure every anomaly aligns with actual human movement dynamics. This cleaned version of SHT can be downloded here.
 [Cleaned ShanghaiTech testset]()

## Citation
If you find our work useful, please consider citing: 


## Contact
If you have any questions or need assistance, please contact the authors at nrashvan@charlotte.edu.


