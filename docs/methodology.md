# Research Methodology Specification

## Project Title
**An Effort-Aware Generative AI Framework for Reducing Cognitive Offloading in Programming Education**

---

## 1. Research Problem & Objectives

In novice programming education, generative AI tools frequently provide complete copy-pasteable solutions upon request. This can cause unreflective cognitive offloading, reducing student problem-solving engagement, leading to over-reliance on automated assistance.

### Primary Research Objective:
Design, implement, and evaluate an **effort-aware generative AI framework** that measures observable engagement proxies and adapts assistance levels (Hint vs. Guided Steps vs. Full Worked Solution) dynamically to mitigate cognitive offloading.

---

## 2. Research Questions (RQs)

- **RQ1:** Can observable interaction signals (code edit diffs, reasoning text, test activity) form an explainable proxy score for student attempt effort?
- **RQ2:** How does effort-aware adaptive scaffolding affect student follow-up concept retention compared to immediate-solution disclosure?
- **RQ3:** Does adaptive scaffolding preserve student autonomy by allowing manual level overrides without trapping users in low-assistance states?

---

## 3. Effort Proxy Formula & Rationale

The effort proxy score $E \in [0, 100]$ is computed as:

$$E = 0.30 \cdot A + 0.25 \cdot C + 0.25 \cdot R + 0.20 \cdot T$$

### Component Rationale:
1. **$A$ (Attempt Completeness, 30%):** Measures whether code contains non-trivial syntax, control loops (`for`/`while`), and return statements.
2. **$C$ (Code Modification Variance, 25%):** Sequence diff ratio relative to starter template.
3. **$R$ (Reasoning Completeness, 25%):** Word count and CS domain conceptual keyword density (*loop*, *condition*, *index*, *return*).
4. **$T$ (Test & Debugging Engagement, 20%):** Documentation of test inputs, expected outputs, and error notes.

> **Methodological Disclaimer:** $E$ is an **observable behavioral proxy score**, not a psychological measure of cognitive capacity or innate student intelligence.

---

## 4. Threats to Validity & Limitations

1. **Construct Validity:** Text length or keyword count may not perfectly reflect mental effort in all students.
2. **External Validity:** Scaffolding performance may vary across different programming paradigms and languages.
3. **Internal Validity:** Offline fallback scaffolds use pre-written domain hints, which differ in variance from live generative model output.
