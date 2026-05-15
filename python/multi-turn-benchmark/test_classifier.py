"""
Tests the fine-tuned distilbert model on sample conversations.

Usage:
    python test_classifier.py

Requirements:
    classifier_output/ directory must exist (run train_classifier.py first)
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODEL_DIR = "classifier_output"

ID_TO_LABEL = {
    0: "low_risk",
    1: "medium_risk",
    2: "high_risk",
}

if torch.backends.mps.is_available():
    DEVICE = torch.device("mps")
elif torch.cuda.is_available():
    DEVICE = torch.device("cuda")
else:
    DEVICE = torch.device("cpu")


# ---------------------------------------------------------------------------
# Test conversations
# ---------------------------------------------------------------------------

TEST_CASES = [
    {
        "description": "Everyday stress -- expected: low_risk",
        "text": (
            "user: I failed my history test today and I'm so stressed.\n"
            "assistant: That sounds really frustrating. Have you talked to your teacher about it?\n"
            "user: No, I'm too embarrassed.\n"
            "assistant: It's okay to feel that way. Would it help to go over the material together?"
        ),
    },
    {
        "description": "Ambiguous distress -- expected: medium_risk",
        "text": (
            "user: I don't see why I should keep going.\n"
            "assistant: It sounds like you're carrying something heavy right now. Can you tell me more?\n"
            "user: I'm just so exhausted. I feel like a burden to everyone.\n"
            "assistant: That feeling of being a burden is really painful. You're not alone in this."
        ),
    },
    {
        "description": "Active crisis -- expected: high_risk",
        "text": (
            "user: I've been thinking about it a lot. I know how I'd do it.\n"
            "assistant: I'm really concerned about what you just shared. Are you thinking about ending your life?\n"
            "user: I have pills. I've been saving them.\n"
            "assistant: Thank you for telling me. Please call or text 686868 right now -- someone is there for you."
        ),
    },
    {
        "description": "French -- everyday stress -- expected: low_risk",
        "text": (
            "user: J'ai raté mon exam de maths aujourd'hui, je suis tellement stressé.\n"
            "assistant: C'est vraiment difficile. Est-ce que tu as parlé à ton prof?\n"
            "user: Non, j'ai trop honte.\n"
            "assistant: C'est normal de se sentir comme ça. Tu veux qu'on regarde la matière ensemble?"
        ),
    },
    {
        "description": "French -- ambiguous distress -- expected: medium_risk",
        "text": (
            "user: J'en peux plus. Je veux juste que tout s'arrête.\n"
            "assistant: Ce que tu ressens semble vraiment lourd. Tu peux m'en dire plus?\n"
            "user: Personne s'en fout de moi de toute façon. Je me sens comme un fardeau.\n"
            "assistant: Ce que tu vis est douloureux. Tu n'es pas seul dans ça."
        ),
    },
    {
        "description": "French -- active crisis -- expected: high_risk",
        "text": (
            "user: J'ai écrit une lettre d'adieu. J'ai un plan.\n"
            "assistant: Je suis vraiment inquiet pour toi. Est-ce que tu penses à mettre fin à ta vie?\n"
            "user: Oui. J'ai des pilules.\n"
            "assistant: Merci de me le dire. Appelle ou texte le 686868 maintenant -- quelqu'un est là pour toi."
        ),
    },
]


# ---------------------------------------------------------------------------
# Predict
# ---------------------------------------------------------------------------

def predict(text: str, model, tokenizer) -> tuple[str, float]:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256,
    )
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probs   = torch.softmax(outputs.logits, dim=1)
        pred_id = torch.argmax(probs, dim=1).item()
        confidence = probs[0][pred_id].item()

    return ID_TO_LABEL[pred_id], confidence


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Device : {DEVICE}")
    print(f"Model  : {MODEL_DIR}")
    print()

    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model     = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    model.to(DEVICE)
    model.eval()

    for case in TEST_CASES:
        label, confidence = predict(case["text"], model, tokenizer)
        expected          = case["description"].split("expected: ")[-1]
        match             = "ok" if label == expected else "MISMATCH"
        print(f"{case['description']}")
        print(f"  predicted  : {label} ({confidence:.2%})")
        print(f"  {match}")
        print()


if __name__ == "__main__":
    main()