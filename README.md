# ESG AI Monitor System

An AI-powered ESG intelligence platform that monitors company-related news and generates analytical ESG risk insights using NLP + Local LLMs.
___

### Overview

This project implements a fully automated ESG monitoring pipeline that fetches corporate news and analyzes it using AI to detect:

ESG relevance

Sentiment trends

Environmental, Social, and Governance risk categories

###Key topics

ESG risk scores

Analytical summaries (not generic news summaries

The system mimics how investment firms and ESG analysts track corporate risk in real time.

### Data Source

News data is collected using NewsAPI:

Source: Public news articles across global publishers
The data is used solely for academic, educational, and evaluation purposes.

Unlike basic news dashboards, this system handles:

AI-powered ESG filtering

Financial sentiment modeling (FinBERT)

Zero-shot ESG classification

Keyword topic extraction

Local LLM ESG analysis (Mistral via Ollama)

Risk scoring engine

Trend analytics

Interactive React dashboard
___
### Features

1. News Ingestion Pipeline

Fetches company-related news articles

Filters only ESG-relevant content

Removes marketing, deals, and noise articles

2. AI ESG Analysis
Sentiment analysis (FinBERT)

ESG category detection (E / S / G)

Topic extraction (KeyBERT)

Analytical ESG summaries using Mistral LLM

3. Risk Scoring Engine

Calculates:

Average sentiment

Negative news ratio

Company ESG Risk Score

4. Metrics Tracking

Daily metrics storage

Sentiment trend tracking

ESG event timeline

5. React Dashboard

Company search

Sentiment trend chart

ESG category pie chart

Trending ESG topics

Article list with AI summaries

Risk score monitoring
___
### Installation & Setup

1.Clone the Repository

`git clone https://github.com/hiayushihere/ESG-AI-MONITOR.git`

`cd esg-ai-monitor`
2. Backend Setup

Create Virtual Environment

`python -m venv venv`

3. Activate Environment

Mac / Linux

`source venv/bin/activate`

Windows

`venv\Scripts\activate`

4.Install Requirements

`pip install -r requirements.txt`

5. Install Ollama (Local AI Engine)

Download:

➡ https://ollama.com/download

Pull Mistral model:

`ollama pull mistral`

Start Ollama server:

`ollama serve`

6. Add API Keys

Update config:

`NEWS_API_KEY=news_api_key`

Database Initialization (First Run Only)

`python`

`>>>from app import create_app, db`

`>>>app = create_app()`

`>>>app.app_context().push()`

`>>>db.create_all()`

`>>>exit()`

Database will be created in:

`instance/database.db`

#### ▶ Run Backend Server

`python -m app.run`

Backend runs at:

`http://127.0.0.1:5000`
___
#### Frontend Setup
1. Navigate to Frontend

`cd frontend`

2. Install Node Dependencies

`npm install`

`npm install axios recharts`

3. Start React App

`npm start`

Frontend runs at:

`http://localhost:3000`
___
### How the System Works

-User enters company name

-Backend fetches ESG-related news

-AI models analyze articles

-LLM generates ESG analytical summaries

-Metrics & risk scores are calculated

-Dashboard visualizes trends and risk
___
### API Endpoints

#### Endpoint	Description

`/fetch/<company>`	Fetch fresh ESG news

`/articles/<company>`	Get AI-analyzed articles

`/metrics/<company>`	Sentiment & risk metrics

`/trending/<company>`	Trending ESG topics

### Tech Stack

Backend → Flask, SQLAlchemy

AI → FinBERT, BART, KeyBERT, Mistral LLM

Frontend → React, Axios, Recharts

Database → SQLite

LLM Runtime → Ollama


