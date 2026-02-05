import re
import google.generativeai as genai
from transformers import pipeline
from app.config import Config
import requests



# ================= CLEAN TEXT =================
def clean_text(text):
    text = re.sub(r"\$\d+[^\s]*", "", text)
    text = re.sub(r"% off|coupon|sale|free shipping", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ================= FINAL AI SUMMARY =================
def generate_summary(company, text, sentiment, category, topics):
    # This prompt forces Mistral 7B to follow professional ESG standards
    prompt = f"""<s>[INST] <<SYS>>
    You are a Senior ESG Investment Analyst. Your goal is to extract only high-value corporate intelligence. 
    <</SYS>>

    Task: Analyze the news context below for {company}.
    
    Rules:
    1. If the news is about a product sale, a toy, or a different company, return: "No significant ESG impact; routine retail/third-party activity."
    2. If it IS relevant, provide a 2-sentence summary highlighting:
       - The specific event (e.g., layoffs, fines, net-zero pledges).
       - The potential long-term impact on {company}'s reputation or operations.
    3. Use professional, neutral language. Do not use fluff like "In this news..."

    Context: {text[:800]}
    
    Analysis: [/INST]</s>"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",  # Ollama maps 'mistral' to 'mistral-7b-instruct-v0.3'
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Lower = more factual, higher = more creative
                    "num_predict": 120,
                    "repeat_penalty": 1.2,
                    "num_ctx": 1024,       # Latency Fix: Smaller memory window
                    "num_thread": 8,       # Latency Fix: Utilize all Mac CPU cores
                    "num_batch": 512,      # Latency Fix: Faster prompt processing
                    "top_k": 20,
                    "top_p": 0.9
                }
            },
            timeout=20
        )
        return response.json().get('response', '').strip()
    except Exception as e:
        return f"Summary pending: {company} {category} update regarding {topics}."