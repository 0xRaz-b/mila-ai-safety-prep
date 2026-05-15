"""
Fine-tuning script -- KHP Youth Crisis Conversation Classifier
Model  : distilbert-base-multilingual-cased
Labels : low_risk, medium_risk, high_risk
Split  : 80/20 train/test
Device : Apple Silicon (MPS)

Usage:
    python train_classifier.py

Requirements:
    pip install transformers torch datasets scikit-learn
"""

import csv
import torch
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    get_linear_schedule_with_warmup,
)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_FILE   = "bilingual_3tier_clean.csv"
MODEL_NAME  = "distilbert-base-multilingual-cased"
OUTPUT_DIR  = "classifier_output"

LABEL_MAP = {
    "low_risk":    0,
    "medium_risk": 1,
    "high_risk":   2,
}
ID_TO_LABEL = {v: k for k, v in LABEL_MAP.items()}

MAX_LENGTH  = 256
BATCH_SIZE  = 8
EPOCHS      = 4
LR          = 2e-5
TEST_SIZE   = 0.20
RANDOM_SEED = 42

# Apple Silicon MPS
if torch.backends.mps.is_available():
    DEVICE = torch.device("mps")
elif torch.cuda.is_available():
    DEVICE = torch.device("cuda")
else:
    DEVICE = torch.device("cpu")


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------

def load_data(path: str) -> tuple[list[str], list[int]]:
    texts, labels = [], []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            label = row.get("label", "").strip()
            text  = row.get("text", "").strip()
            if label in LABEL_MAP and text:
                texts.append(text)
                labels.append(LABEL_MAP[label])
    return texts, labels


class ConversationDataset(Dataset):
    def __init__(self, texts: list[str], labels: list[int], tokenizer):
        self.encodings = tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=MAX_LENGTH,
            return_tensors="pt",
        )
        self.labels = torch.tensor(labels, dtype=torch.long)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return {
            "input_ids":      self.encodings["input_ids"][idx],
            "attention_mask": self.encodings["attention_mask"][idx],
            "labels":         self.labels[idx],
        }


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

def train_epoch(model, loader, optimizer, scheduler):
    model.train()
    total_loss = 0

    for batch in loader:
        optimizer.zero_grad()
        input_ids      = batch["input_ids"].to(DEVICE)
        attention_mask = batch["attention_mask"].to(DEVICE)
        labels         = batch["labels"].to(DEVICE)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss    = outputs.loss
        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()

        total_loss += loss.item()

    return total_loss / len(loader)


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def evaluate(model, loader) -> tuple[float, list[int], list[int]]:
    model.eval()
    all_preds, all_labels = [], []

    with torch.no_grad():
        for batch in loader:
            input_ids      = batch["input_ids"].to(DEVICE)
            attention_mask = batch["attention_mask"].to(DEVICE)
            labels         = batch["labels"].to(DEVICE)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            preds   = torch.argmax(outputs.logits, dim=1)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    accuracy = np.mean(np.array(all_preds) == np.array(all_labels))
    return accuracy, all_preds, all_labels


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Device : {DEVICE}")
    print(f"Model  : {MODEL_NAME}")
    print()

    # Load data
    texts, labels = load_data(DATA_FILE)
    print(f"Loaded {len(texts)} conversations.")

    # Split
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts, labels,
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
        stratify=labels,
    )
    print(f"Train  : {len(train_texts)}")
    print(f"Test   : {len(test_texts)}")
    print()

    # Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # Datasets
    train_dataset = ConversationDataset(train_texts, train_labels, tokenizer)
    test_dataset  = ConversationDataset(test_texts,  test_labels,  tokenizer)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader  = DataLoader(test_dataset,  batch_size=BATCH_SIZE, shuffle=False)

    # Model
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(LABEL_MAP),
    )
    model.to(DEVICE)

    # Optimizer and scheduler
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)
    total_steps = len(train_loader) * EPOCHS
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=int(0.1 * total_steps),
        num_training_steps=total_steps,
    )

    # Training loop
    for epoch in range(1, EPOCHS + 1):
        train_loss = train_epoch(model, train_loader, optimizer, scheduler)
        accuracy, _, _ = evaluate(model, test_loader)
        print(f"Epoch {epoch}/{EPOCHS}  loss={train_loss:.4f}  accuracy={accuracy:.4f}")

    # Final evaluation
    print()
    _, preds, true_labels = evaluate(model, test_loader)
    print(classification_report(
        true_labels, preds,
        target_names=["low_risk", "medium_risk", "high_risk"],
    ))

    # Save model
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(exist_ok=True)
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)
    print(f"Model saved to {output_path.absolute()}")


if __name__ == "__main__":
    main()
