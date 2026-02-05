from transformers import pipeline
from keybert import KeyBERT
import warnings
warnings.filterwarnings("ignore")

# Models
sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")
category_pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
kw_model = KeyBERT()

def is_esg_related(text):
    """
    Two-stage filter: 
    1. Fast Keyword check (CPU efficient)
    2. Deep AI check (Context aware)
    """
    # Stage 1: Fast Keyword Scan
    keywords = ['carbon', 'climate', 'layoff', 'diversity', 'governance', 'lawsuit', 'ethics', 
                'emissions', 'sustainability', 'workforce', 'board', 'regulatory', 'environmental']
    if any(word in text.lower() for word in keywords):
        return True
        
    # Stage 2: Loosen the AI verification score from 0.6 to 0.4
    res = category_pipeline(text[:400], candidate_labels=["ESG related", "General News"])
    return res['labels'][0] == "ESG related" and res['scores'][0] > 0.4 # Lowered threshold

def analyze_article(text):
    # 1. First, check relevance. If it fails, we return early to save latency.
    if not is_esg_related(text):
        return None, None, "Non-ESG", None

    # 2. Sentiment (Focused on the lead text)
    sent = sentiment_pipeline(text[:512])[0]
    sentiment = sent["label"].lower()
    score = float(sent["score"])

    # 3. Categorization (Clean labels for better Zero-Shot accuracy)
    labels = ["Environmental", "Social", "Governance"]
    cat = category_pipeline(text[:600], labels)
    category = cat["labels"][0]

    # 4. Topics
    keywords = kw_model.extract_keywords(text, top_n=3, keyphrase_ngram_range=(1, 1), stop_words='english')
    topics = ", ".join(k[0] for k in keywords)

    return sentiment, score, category, topics