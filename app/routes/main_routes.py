from flask import Blueprint
from app.services.news_service import fetch_news_for_company
from app.models.models import Article, AIAnalysis, DailyMetric, Company
from sqlalchemy import func
from app import db
main = Blueprint('main', __name__)

@main.route("/")
def home():
    return {"message": "ESG AI Monitor is Running "}

@main.route("/fetch/<company>")
def fetch_news(company):
    from app.models.models import Company, Article, AIAnalysis
    
    # Force delete existing records first and COMMIT
    comp = Company.query.filter(func.lower(Company.name) == company.lower()).first()
    if comp:
        # Delete metrics and articles (AIAnalysis usually cascades or delete manually)
        AIAnalysis.query.filter(AIAnalysis.article_id.in_(
            db.session.query(Article.id).filter_by(company_id=comp.id)
        )).delete(synchronize_session=False)
        Article.query.filter_by(company_id=comp.id).delete()
        db.session.commit() # <--- CRITICAL: Commit the wipe before fetching
    
    # Now fetch fresh
    fetch_news_for_company(company)
    return {"status": f"Data refreshed for {company}"}
@main.route("/articles/<company>")
def get_articles(company):
    from app.models.models import Company

    comp = Company.query.filter(func.lower(Company.name) == company.lower()).first()

    if not comp:
        return {"error": "Company not found"}

    articles = Article.query.filter_by(company_id=comp.id).all()

    results = []
    for article in articles:
        ai = AIAnalysis.query.filter_by(article_id=article.id).first()
        results.append({
            "title": article.title,
            "source": article.source,
            "date": article.published_at,
            "sentiment": ai.sentiment if ai else None,
            "sentiment_score": ai.sentiment_score if ai else None,
            "category": ai.category if ai else None,
            "summary": ai.summary if ai else None,
            "topics": ai.topics if ai else None
        })

    return {"articles": results}
@main.route("/metrics/<company>")
def get_metrics(company):
    from sqlalchemy import func

    comp = Company.query.filter(func.lower(Company.name) == company.lower()).first()
    if not comp:
        return {"error": "Company not found"}

    metrics = DailyMetric.query.filter_by(company_id=comp.id).all()

    return {
        "metrics": [
            {
                "date": m.date.strftime("%Y-%m-%d"),
                "avg_sentiment": m.avg_sentiment,
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

    topics = db.session.query(AIAnalysis.topics).join(Article)\
        .filter(Article.company_id == comp.id).all()

    from collections import Counter

    all_words = []
    for t in topics:
        if t[0]:
            all_words.extend(t[0].split(", "))

    top = Counter(all_words).most_common(5)

    return {"trending_topics": top}
