from sqlalchemy import func, case
from app.models.models import Article, AIAnalysis, DailyMetric
from app import db
from datetime import date

def calculate_daily_metrics(company_id):
    today = date.today()

    # Clear existing to avoid duplicates
    db.session.query(DailyMetric).filter_by(company_id=company_id, date=today).delete()

    # Query metrics for articles published TODAY
    data = db.session.query(
        func.avg(AIAnalysis.sentiment_score),
        func.sum(case((AIAnalysis.sentiment == "negative", 1), else_=0)),
        func.sum(case((AIAnalysis.sentiment == "positive", 1), else_=0)),
        func.sum(case((AIAnalysis.sentiment == "neutral", 1), else_=0)),
        func.count(AIAnalysis.id)
    ).join(Article, AIAnalysis.article_id == Article.id)\
     .filter(Article.company_id == company_id)\
     .filter(func.date(Article.published_at) == today).first()

    avg_raw, neg, pos, neu, total = data

    if not total or total == 0:
        return

    # --- LATENCY & WEIRD SENTIMENT FIX: BAYESIAN SMOOTHING ---
    # We add 5 'virtual' neutral articles to keep the score grounded.
    # This prevents the chart from jumping to 1.0 or 0.0 with low volume.
    smoothing_factor = 5
    avg_sentiment = (float(avg_raw or 0) * total) / (total + smoothing_factor)

    # Risk Score logic: Weighting negatives heavily
    neg_ratio = (neg / total)
    risk_score = min(100, (neg_ratio * 85) + ((neg or 0) * 3))

    metric = DailyMetric(
        company_id=company_id,
        date=today,
        avg_sentiment=round(avg_sentiment, 4),
        negative_count=int(neg or 0),
        positive_count=int(pos or 0),
        neutral_count=int(neu or 0),
        total_articles=int(total),
        risk_score=float(risk_score)
    )

    db.session.add(metric)
    db.session.commit()