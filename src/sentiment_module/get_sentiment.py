##################################################
# Module E - Sentiment Engine (FinBERT)
# Author: Patric Dahinden
# Python version: 3.13.x (project standard)
#
# Note: GitHub Copilot was used for coding efficiency,
# structure, coherence, and layout.
#
# Description:
# Receives a list of news articles (dictionaries), uses the
# FinBERT model to classify sentiment, and adds BUY/HOLD/SELL
# labels with confidence scores.
#
# Requirements:
# - pip install transformers torch --upgrade
##################################################

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# -----------------------------
# 1. LOAD MODEL ONCE AT START
# -----------------------------

# Name of the FinBERT model (from HuggingFace)
MODEL_NAME = "ProsusAI/finbert"

# Load tokenizer: turns text into numbers (token IDs)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Load the actual FinBERT model (a neural network)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Put the model into evaluation mode (important for inference)
model.eval()

# Choose device: GPU if available, otherwise CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Mapping from model class index to text label
# FinBERT uses: 0 = negative, 1 = neutral, 2 = positive
id2label = {0: "negative", 1: "neutral", 2: "positive"}


# -----------------------------------
# 2. HELPER: BUILD TEXT FROM ARTICLE
# -----------------------------------

def build_text_from_article(article):
    """
    Combine title and summary into one text string.

    article: dictionary with at least keys "title" and "summary"

    returns: string that will be sent to FinBERT
    """
    title = article.get("title", "")
    summary = article.get("summary", "")

    # Join title and summary. If one is empty, this still works.
    text = (title + ". " + summary).strip()
    return text


# -----------------------------------
# 3. HELPER: PREDICT SENTIMENT
# -----------------------------------

def predict_sentiment_for_text(text):
    """
    Run FinBERT on a single text string.

    returns a dictionary with:
        - sentiment: "BUY" / "HOLD" / "SELL"
        - raw_label: "positive" / "neutral" / "negative"
        - score: confidence value between 0 and 1
    """
    # If the text is empty, we return a neutral result
    if not text:
        return {
            "sentiment": "HOLD",
            "raw_label": "neutral",
            "score": 0.0
        }

    # Tokenize the text: convert to input IDs for the model
    inputs = tokenizer(
        text,
        truncation=True,        # cut long texts
        padding=True,           # pad to same length (only 1 text here)
        return_tensors="pt"     # return PyTorch tensors
    )

    # Move input tensors to same device as the model
    inputs = {key: value.to(device) for key, value in inputs.items()}

    # We only want predictions, no gradients (faster and safer)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits  # raw scores for each class

    # Convert raw scores to probabilities with softmax
    probs = torch.softmax(logits, dim=1)[0].cpu().numpy()

    # Index of highest probability
    best_class_id = int(probs.argmax())
    raw_label = id2label[best_class_id]
    confidence = float(probs[best_class_id])

    # Map raw_label to BUY / HOLD / SELL
    if raw_label == "positive":
        decision = "BUY"
    elif raw_label == "neutral":
        decision = "HOLD"
    else:
        decision = "SELL"

    return {
        "sentiment": decision,
        "raw_label": raw_label,
        "score": round(confidence, 4)
    }


# -----------------------------------
# 4. MAIN FUNCTION FOR MODULE E
# -----------------------------------

def analyze_articles(articles):
    """
    Enrich a list of article dicts with sentiment fields.
    """
    result = []

    for article in articles:
        text = build_text_from_article(article)
        prediction = predict_sentiment_for_text(text)

        new_article = article.copy()
        new_article["sentiment"] = prediction["sentiment"]
        new_article["raw_label"] = prediction["raw_label"]
        new_article["score"] = prediction["score"]

        result.append(new_article)

    return result


# -----------------------------------
# 5. SIMPLE TEST
# -----------------------------------

if __name__ == "__main__":
    example_articles = [
        {
            "title": "Apple announces new product line",
            "summary": "Apple introduced a new device expected to boost sales...",
            "published": "2024-01-15"
        },
        {
            "title": "iPhone demand weakens",
            "summary": "Analysts see reduced demand in important markets...",
            "published": "2024-01-20"
        }
    ]

    enriched = analyze_articles(example_articles)

    for art in enriched:
        print(art["published"], "|", art["title"])
        print("  SENTIMENT:", art["sentiment"],
              "| raw:", art["raw_label"],
              "| score:", art["score"])
        print()
