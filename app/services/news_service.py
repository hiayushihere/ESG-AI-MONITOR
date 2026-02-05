import requests
from datetime import datetime, timedelta
from app.models.models import Article, Company, AIAnalysis
from app import db
from app.config import Config
from app.ai.nlp_pipeline import analyze_article, is_esg_related
from app.ai.local_summary import generate_summary
from app.services.metrics_service import calculate_daily_metrics

def fetch_news_for_company(company_name, days=5):
    start_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    categories_queries = {
        "Environmental": f'"{company_name}" (emissions OR carbon OR climate OR sustainability OR "net zero")',
        "Social": f'"{company_name}" (layoffs OR "labor rights" OR diversity OR employees OR "human rights")',
        "Governance": f'"{company_name}" (governance OR lawsuit OR ethics OR board OR "regulatory")'
    }

    company = Company.query.filter_by(name=company_name).first()
    if not company:
        company = Company(name=company_name)
        db.session.add(company)
        db.session.commit()

    all_articles_data = [] # To collect articles from all passes
    seen_titles = set()

    # Pass 1: Pillar Specific Search
    for pillar, query in categories_queries.items():
        params = {
            "q": query,
            "from": start_date,
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": 40,
            "apiKey": Config.NEWS_API_KEY
        }
        try:
            response = requests.get("https://newsapi.org/v2/everything", params=params)
            articles = response.json().get("articles", [])
            for a in articles:
                if a.get("title") not in seen_titles:
                    all_articles_data.append((a, pillar))
                    seen_titles.add(a.get("title"))
        except Exception as e:
            print(f"API Error: {e}")

    # Pass 2: Fallback (If we found < 15 articles, broaden the search)
    if len(all_articles_data) < 15:
        fallback_query = f'"{company_name}" (ESG OR sustainability OR corporate OR news)'
        try:
            res = requests.get("https://newsapi.org/v2/everything", 
                               params={"q": fallback_query, "language": "en", "pageSize": 50, "apiKey": Config.NEWS_API_KEY})
            for a in res.json().get("articles", []):
                if a.get("title") not in seen_titles:
                    all_articles_data.append((a, "General"))
                    seen_titles.add(a.get("title"))
        except: pass

    # Processing & Saving
    total_added = 0
    for art, expected_pillar in all_articles_data:
        title = art.get("title")
        if not title or Article.query.filter_by(title=title).first():
            continue

        text = f"{title}. {art.get('description', '')}"
        
        # AI Relevance Filter
        if not is_esg_related(text):
            continue

        try:
            sentiment, score, category, topics = analyze_article(text)
            if sentiment is None: continue # Skip if filter rejects

            final_cat = expected_pillar if category == "Non-ESG" else category
            summary = generate_summary(company_name, text, sentiment, final_cat, topics)

            new_article = Article(
                company_id=company.id,
                title=title,
                content=text,
                source=art["source"]["name"],
                published_at=datetime.strptime(art["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
            )
            db.session.add(new_article)
            db.session.flush()

            db.session.add(AIAnalysis(
                article_id=new_article.id,
                sentiment=sentiment,
                sentiment_score=score,
                category=final_cat,
                summary=summary,
                topics=topics
            ))
            total_added += 1

        except Exception as e:
            print(f"DB Error: {e}")
            db.session.rollback()

    db.session.commit()
    calculate_daily_metrics(company.id)
    print(f"Success: Added {total_added} articles for {company_name}.")