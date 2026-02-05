from flask import Blueprint, jsonify
from app.services.news_service import fetch_news_for_company
from app.services.alerts_service import get_risk_status 
from app.models.models import Article, AIAnalysis, DailyMetric, Company
from sqlalchemy import func
from app import db
from collections import Counter

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return {"message": "ESG AI Monitor is Running"}

@main.route("/risk/<company>")
def fetch_risk(company):
    comp = Company.query.filter(func.lower(Company.name) == company.lower()).first()
    if not comp:
        return jsonify({"level": "NEW", "message": "Ready for initial analysis", "color": "#3b82f6"})
    
    # Calls the logic for the dynamic alert banner
    status = get_risk_status(comp.id)
    return jsonify(status)

@main.route("/fetch/<company>")
def fetch_news(company):
    comp = Company.query.filter(func.lower(Company.name) == company.lower()).first()
    if comp:
        # Wipe existing data to ensure the refresh is truly "fresh"
        AIAnalysis.query.filter(AIAnalysis.article_id.in_(
            db.session.query(Article.id).filter_by(company_id=comp.id)
        )).delete(synchronize_session=False)
        Article.query.filter_by(company_id=comp.id).delete()
        db.session.commit()
    
    fetch_news_for_company(company)
    return {"status": "success", "message": f"Data refreshed for {company}"}

@main.route("/articles/<company>")
def get_articles(company):
    comp = Company.query.filter(func.lower(Company.name) == company.lower()).first()
    if not comp:
        return {"error": "Company not found"}

    articles = Article.query.filter_by(company_id=comp.id).all()

    results = []
    total_conf = 0
    count = 0

    for article in articles:
        ai = AIAnalysis.query.filter_by(article_id=article.id).first()
        score = ai.sentiment_score if (ai and ai.sentiment_score) else 0
        
        results.append({
            "title": article.title,
            "source": article.source,
            "date": article.published_at.strftime("%b %d, %Y") if article.published_at else None,
            "sentiment": ai.sentiment if ai else "neutral",
            "sentiment_score": score,
            "category": ai.category if ai else "General",
            "summary": ai.summary if ai else "No summary available.",
            "topics": ai.topics if ai else ""
        })
        
        # Aggregate confidence data
        total_conf += score
        count += 1

    # Calculate overall AI Confidence percentage
    overall_confidence = round((total_conf / count) * 100, 1) if count > 0 else 0

    return {
        "articles": results,
        "overall_confidence": overall_confidence
    }

@main.route("/metrics/<company>")
def get_metrics(company):
    comp = Company.query.filter(func.lower(Company.name) == company.lower()).first()
    if not comp:
        return {"error": "Company not found"}

    metrics = DailyMetric.query.filter_by(company_id=comp.id).order_by(DailyMetric.date.asc()).all()

    return {
        "metrics": [
            {
                "date": m.date.strftime("%m/%d"), # Cleaner date for charts
                "avg_sentiment": round(m.avg_sentiment, 2),
                "negative_articles": m.negative_count,
                "positive_articles": m.positive_count,
                "neutral_articles": m.neutral_count,
                "total_articles": m.total_articles,
                "risk_score": m.risk_score
            } for m in metrics
        ]
    }

@main.route("/trending/<company>")
def trending_topics(company):
    comp = Company.query.filter(func.lower(Company.name) == company.lower()).first()
    if not comp:
        return {"error": "Company not found"}

    topics_query = db.session.query(AIAnalysis.topics).join(Article)\
        .filter(Article.company_id == comp.id).all()

    all_words = []
    for t in topics_query:
        if t[0]:
            # Split by comma and clean whitespace
            words = [w.strip() for w in t[0].split(",")]
            all_words.extend(words)

    # Return top 8 for a more colorful UI tag cloud
    top = Counter(all_words).most_common(8)

    return {"trending_topics": top}