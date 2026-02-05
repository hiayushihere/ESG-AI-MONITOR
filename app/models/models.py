from app import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    title = db.Column(db.String(300))
    content = db.Column(db.Text)
    source = db.Column(db.String(200))
    published_at = db.Column(db.DateTime)

class AIAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    sentiment = db.Column(db.String(20))
    sentiment_score = db.Column(db.Float)
    category = db.Column(db.String(50))
    summary = db.Column(db.Text)
    topics = db.Column(db.String(300))

class DailyMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)
    date = db.Column(db.Date)
    avg_sentiment = db.Column(db.Float)
    negative_count = db.Column(db.Integer)
    positive_count = db.Column(db.Integer)
    neutral_count = db.Column(db.Integer)
    total_articles = db.Column(db.Integer)
    risk_score = db.Column(db.Float)

