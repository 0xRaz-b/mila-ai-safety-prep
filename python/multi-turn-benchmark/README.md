# Multi-Turn Benchmark

This project explores turn-by-turn risk detection in youth mental health conversations. The goal is to classify each turn of a conversation in real time rather than analyzing the conversation as a whole at the end.

---

## Classifier Experiments

The first phase tested off-the-shelf models to see if any could reliably detect escalating distress without fine-tuning.

| Model | Approach | Result |
|---|---|---|
| `unitary/toxic-bert` | Toxicity detection | All turns flagged high regardless of content. Detects insults, not distress. |
| `j-hartmann/emotion-english-distilroberta-base` | Emotion classification | More nuanced, but "I don't see why I should keep going" classified as LOW (surprise, 0.663). Critical false negative. |
| `martin-ha/toxic-comment-model` | Toxic comment detection | Opposite problem — all turns classified LOW with high confidence. |

General-purpose models consistently fail on self harm language because it does not read as toxic in the traditional sense. A labelled dataset and fine-tuned classifier are needed.

---

## Synthetic Dataset Generation

A three-tier classification scheme was used: low_risk, medium_risk, and high_risk. The medium tier captures the ambiguous language that sits between everyday stress and active crisis — the zone where early intervention matters most.

**Generation setup**

- Model: `qwen2.5vl:latest` via Ollama (switched from `gemma4:31b` after persistent JSON truncation issues)
- Target: 600 conversations, 200 per tier, 70% English / 30% French
- Hardware: Apple Silicon M5 Max, Metal GPU

`gemma4:31b` was the first choice given its general language quality, but it produced frequent JSON truncation even after increasing `num_predict` to 32768. `qwen2.5vl` resolved the truncation at the cost of ignoring turn count constraints — conversations regularly exceeded 30 turns.

**Generation results**

| Status | Count |
|---|---|
| Generated | 548 |
| Failed | 52 |

---

## Dataset Cleaning

Conversations outside the 6-30 turn range were removed using SQL (PostgreSQL). The aberrant values — some reaching 307 turns — came from `qwen2.5vl` ignoring the prompt constraints on certain runs.

| | Count |
|---|---|
| Before cleaning | 548 |
| After cleaning | 474 |
| Removed | 74 |

**Final distribution**

| Tier | EN | FR | Total |
|---|---|---|---|
| low_risk | 132 | 51 | 183 |
| medium_risk | 114 | 49 | 163 |
| high_risk | 76 | 52 | 128 |

Average turns: 20.1. Turn range: 6 to 30.

The high_risk tier is underrepresented relative to the others, likely because those conversations — involving specific methods or plans — triggered more timeouts and generation failures.