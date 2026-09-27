# Experimental Evaluation Protocol

## Project Title
**An Effort-Aware Generative AI Framework for Reducing Cognitive Offloading in Programming Education**

---

## 1. Experimental Design (A/B/C Testing)

To evaluate the efficacy of effort-aware scaffolding in mitigating cognitive offloading, a between-subjects experimental trial protocol is established across three experimental conditions:

| Condition | Assistance Policy | Description |
| :--- | :--- | :--- |
| **Condition A (Control)** | Immediate Solution | Revealing full reference code & explanation on first request. |
| **Condition B (Fixed)** | Fixed Progressive Hints | Static sequence: Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Solution regardless of effort. |
| **Condition C (Adaptive)** | Effort-Aware Scaffolding | Level 1, 2, or 3 selected dynamically via Effort Proxy Score $E$. |

---

## 2. Measurable Primary Outcomes

1. **Follow-Up Concept Accuracy (%):** Proportion of correct responses on post-problem conceptual questions.
2. **First-Attempt Completeness:** Proportion of initial attempts meeting structural criteria.
3. **Number of Attempts to Mastery:** Total trial count required to reach correct solution.
4. **Time on Task (seconds):** Total duration spent actively engaged on problem.

---

## 3. Human Ethics & Privacy Protocol

- Participant participation must be voluntary with informed consent.
- All stored interaction logs utilize anonymous `session_id` identifiers.
- No personally identifiable information (PII), student IDs, or email addresses are stored in database records.
- Local SQLite database provides a one-click history purge option.
