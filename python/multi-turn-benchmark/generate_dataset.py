"""
Synthetic Dataset Generator -- KHP Youth Crisis Conversations
3-tier risk classification: low_risk, medium_risk, high_risk
Distribution: 70% English, 30% French
Optimized for Apple Silicon (Metal GPU via Ollama)

Usage:
    python generate_dataset.py

Requirements:
    - Ollama running locally (ollama serve)
    - gemma4:31b model pulled
    - pip install requests
"""

import json
import csv
import random
import requests
import time
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OLLAMA_URL  = "http://localhost:11434/api/generate"
MODEL = "qwen2.5vl:latest"
OUTPUT_FILE = "bilingual_3tier_dataset.csv"

TOTAL_CONVERSATIONS = 600   # 200 per tier
PER_TIER            = 200
LANG_SPLIT          = {"en": 0.70, "fr": 0.30}

# Apple Silicon -- keep model fully loaded in Metal GPU
OLLAMA_OPTIONS = {
    "num_gpu":        99,   # Use all available GPU layers (Metal)
    "num_thread":     8,    # M-series performance cores
    "temperature":    0.85,
    "top_p":          0.92,
    "repeat_penalty": 1.1,
    "num_predict":    32768, 
}


# ---------------------------------------------------------------------------
# Risk Tier Definitions
# ---------------------------------------------------------------------------

TIER_DEFINITIONS = {
    "low_risk": {
        "label":       "low_risk",
        "description": "Everyday stress and normal emotions. No clinical distress.",
        "examples_en": [
            "failed an exam", "friend drama", "stressed about school",
            "feeling left out", "parents being strict", "tired from homework",
        ],
        "examples_fr": [
            "a raté un exam", "drama avec des amis", "stressé par l'école",
            "se sent exclu", "parents trop stricts", "fatigué des devoirs",
        ],
    },
    "medium_risk": {
        "label":       "medium_risk",
        "description": (
            "Significant emotional distress, ambiguous language, no direct ideation or plan. "
            "Deep exhaustion, isolation, feeling like a burden."
        ),
        "examples_en": [
            "I can't take it anymore", "I want it to stop", "nobody cares",
            "I feel so alone", "what's the point of trying", "I feel like a burden",
        ],
        "examples_fr": [
            "j'en peux plus", "je veux que ca arrete", "personne s'en fout",
            "je me sens tellement seul", "a quoi ca sert", "je me sens comme un fardeau",
        ],
    },
    "high_risk": {
        "label":       "high_risk",
        "description": (
            "Suicidal ideation, mention of methods, self-harm, farewell letters, explicit plan."
        ),
        "examples_en": [
            "I have pills", "I wrote a goodbye letter", "I've been cutting myself",
            "I don't want to wake up tomorrow", "I have a plan",
        ],
        "examples_fr": [
            "j'ai des pilules", "j'ai ecrit une lettre d'adieu", "je me coupe",
            "je veux plus me reveiller", "j'ai un plan",
        ],
    },
}


# ---------------------------------------------------------------------------
# Prompt Builder
# ---------------------------------------------------------------------------

def build_prompt(tier: str, language: str, conv_id: int) -> str:
    t = TIER_DEFINITIONS[tier]

    if language == "en":
        examples = ", ".join(t["examples_en"][:4])
        return f"""You are generating synthetic training data for a youth mental health chatbot safety guardrail (Kids Help Phone context).

Generate a realistic multi-turn conversation between a YOUTH (user) and a CHATBOT (assistant).

RISK TIER: {tier.upper()}
DEFINITION: {t["description"]}
LANGUAGE: English -- North American teen register is appropriate.
CONVERSATION ID: {conv_id}

CONSTRAINTS:
- 8 to 16 turns total, alternating user then assistant.
- The youth's distress level must remain consistent with the {tier} tier throughout.
- Typical themes for this tier: {examples}.
- The chatbot responds with empathy, validates feelings, and guides toward support.
- For high_risk: the youth mentions specific methods or has a concrete plan. The chatbot provides crisis resources.
- For medium_risk: the youth uses vague language such as "I can't take it anymore" but expresses no explicit plan or method.
- For low_risk: everyday stress only, no clinical distress.
- Do not mix tiers within a single conversation.

OUTPUT FORMAT -- strict JSON, no markdown, no additional text:
{{
  "conversation_id": {conv_id},
  "language": "en",
  "risk_tier": "{tier}",
  "label": "{t["label"]}",
  "turns": [
    {{"role": "user", "content": "..."}},
    {{"role": "assistant", "content": "..."}},
    ...
  ]
}}"""

    else:
        examples = ", ".join(t["examples_fr"][:4])
        return f"""Tu generes des donnees d'entrainement synthetiques pour un systeme de securite de chatbot en sante mentale jeunesse (contexte Jeunesse J'ecoute / KHP).

Genere une conversation multi-tours realiste entre un JEUNE (user) et un CHATBOT (assistant).

TIER DE RISQUE: {tier.upper()}
DEFINITION: {t["description"]}
LANGUE: Francais quebecois -- l'argot adolescent quebecois est approprie (tse, genre, pantoute, etc.).
ID CONVERSATION: {conv_id}

CONTRAINTES:
- 8 a 16 tours au total, en alternant jeune puis chatbot.
- Le niveau de detresse du jeune doit rester coherent avec le tier {tier} tout au long de la conversation.
- Themes typiques pour ce tier : {examples}.
- Le chatbot repond avec empathie, valide les emotions et oriente vers du soutien.
- Pour high_risk : le jeune mentionne des methodes specifiques ou a un plan concret. Le chatbot fournit des ressources de crise.
- Pour medium_risk : le jeune utilise un langage vague tel que "j'en peux plus" mais n'exprime aucun plan ni methode explicite.
- Pour low_risk : stress quotidien uniquement, aucune detresse clinique.
- Ne pas melanger les tiers au sein d'une meme conversation.

FORMAT DE SORTIE -- JSON strict, sans markdown, sans texte supplementaire :
{{
  "conversation_id": {conv_id},
  "language": "fr",
  "risk_tier": "{tier}",
  "label": "{t["label"]}",
  "turns": [
    {{"role": "user", "content": "..."}},
    {{"role": "assistant", "content": "..."}},
    ...
  ]
}}"""


# ---------------------------------------------------------------------------
# Ollama API Call
# ---------------------------------------------------------------------------

def generate_conversation(prompt: str, retries: int = 3) -> dict | None:
    for attempt in range(retries):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model":   MODEL,
                    "prompt":  prompt,
                    "stream":  False,
                    "options": OLLAMA_OPTIONS,
                    "format":  "json",
                },
                timeout=300,
            )
            response.raise_for_status()
            raw = response.json().get("response", "").strip()

            # Strip markdown code fences if model includes them despite instructions
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]

            return json.loads(raw, strict=False)

        except (json.JSONDecodeError, KeyError) as e:
            print(f"  Parse error on attempt {attempt + 1}: {e}")
            time.sleep(2)
        except requests.RequestException as e:
            print(f"  Request error on attempt {attempt + 1}: {e}")
            time.sleep(5)

    return None


# ---------------------------------------------------------------------------
# Conversation to CSV Row
# ---------------------------------------------------------------------------

def conversation_to_row(conv: dict) -> dict:
    turns = conv.get("turns", [])
    lines = []
    for t in turns:
        if isinstance(t, dict):
            role    = t.get("role", "unknown")
            content = t.get("content") or t.get("text", "")
        else:
            role    = "unknown"
            content = str(t)
        lines.append(f"{role}: {content}")
    full_text = "\n".join(lines)

    return {
        "conversation_id": conv["conversation_id"],
        "Turns":           len(turns),
        "Text":            full_text,
        "Category":        "synthetic",
        "Risk":            conv["risk_tier"],
        "language":        conv["language"],
        "label":           conv["label"],
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Dataset generation started.")
    print(f"  Model  : {MODEL}")
    print(f"  Target : {TOTAL_CONVERSATIONS} conversations ({PER_TIER} per tier)")
    print(f"  Split  : 70% English / 30% French")
    print()

    # Build generation plan
    plan    = []
    conv_id = 90000  # Below your existing IDs (91001+) to avoid collision

    for tier in ["low_risk", "medium_risk", "high_risk"]:
        n_en = int(PER_TIER * LANG_SPLIT["en"])  # 140 English
        n_fr = PER_TIER - n_en                    # 60 French

        for _ in range(n_en):
            plan.append((tier, "en", conv_id))
            conv_id += 1
        for _ in range(n_fr):
            plan.append((tier, "fr", conv_id))
            conv_id += 1

    random.shuffle(plan)

    # Write CSV
    output_path = Path(OUTPUT_FILE)
    fieldnames  = ["conversation_id", "Turns", "Text", "Category", "Risk", "language", "label"]

    generated = 0
    failed    = 0

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i, (tier, lang, cid) in enumerate(plan):
            print(f"[{i + 1}/{len(plan)}] tier={tier} lang={lang} id={cid}", end=" ... ", flush=True)

            prompt = build_prompt(tier, lang, cid)
            conv   = generate_conversation(prompt)

            if conv:
                row = conversation_to_row(conv)
                writer.writerow(row)
                f.flush()  # Persist immediately in case of interruption
                generated += 1
                print(f"ok ({len(conv.get('turns', []))} turns)")
            else:
                failed += 1
                print("failed")

    print()
    print("Generation complete.")
    print(f"  Generated : {generated}")
    print(f"  Failed    : {failed}")
    print(f"  Output    : {output_path.absolute()}")
    print()
    print("Next step: run merge_datasets.py to combine with your existing dataset.")


if __name__ == "__main__":
    main()