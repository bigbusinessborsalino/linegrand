import os
import itertools
import time
from datetime import datetime
from google import genai
from groq import Groq
import cohere
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# --- 1. MONGODB SETUP ---
# Connects to the exact same database your Broadcaster uses!
MONGO_URI = os.getenv("MONGO_URI")
db_client = MongoClient(MONGO_URI) if MONGO_URI is not None else None
db = db_client.grandline_news if db_client is not None else None
articles_collection = db.articles if db is not None else None

# --- 2. THE PERFECT 1-TO-10 LOAD BALANCER ---
available_clients = []

for i in range(1, 11):
    gem_key = os.getenv(f"GEMINI_API_KEY_{i}")
    if gem_key and gem_key.strip():
        try:
            client = genai.Client(api_key=gem_key.strip())
            available_clients.append({"engine": "gemini", "client": client, "key_id": f"GEMINI_API_KEY_{i}"})
        except Exception as e:
            print(f"Failed to load GEMINI_API_KEY_{i}: {e}")

    groq_key = os.getenv(f"GROQ_API_KEY_{i}")
    if groq_key and groq_key.strip():
        try:
            client = Groq(api_key=groq_key.strip())
            available_clients.append({"engine": "groq", "client": client, "key_id": f"GROQ_API_KEY_{i}"})
        except Exception as e:
            print(f"Failed to load GROQ_API_KEY_{i}: {e}")

    coh_key = os.getenv(f"COHERE_API_KEY_{i}")
    if coh_key and coh_key.strip():
        try:
            client = cohere.Client(coh_key.strip())
            available_clients.append({"engine": "cohere", "client": client, "key_id": f"COHERE_API_KEY_{i}"})
        except Exception as e:
            print(f"Failed to load COHERE_API_KEY_{i}: {e}")

if not available_clients:
    print("❌ CRITICAL ERROR: NO API KEYS FOUND AT ALL! The bot cannot write.")

engine_cycle = itertools.cycle(available_clients)
print(f"🚀 MEGA-POOL INITIALIZED: {len(available_clients)} AI Engines loaded in perfect sequence!")

# --- 3. CORE BOT LOGIC ---

def write_news_article(source_url, topic):
    """Writes an article using the next available AI engine in the sorted pool."""
    worker = next(engine_cycle)
    engine_name = worker["engine"]
    client = worker["client"]
    key_id = worker["key_id"]
    
    print(f"🧠 Brain Selected: {engine_name.upper()} (Powered by {key_id})")
    time.sleep(2) 
    
    prompt = f"Write a 300-word exciting news article about {topic}. Be professional but engaging. Format in clean paragraphs, no markdown."
    
    try:
        if engine_name == "gemini":
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            return response.text
        elif engine_name == "groq":
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content
        elif engine_name == "cohere":
            response = client.chat(message=prompt)
            return response.text
    except Exception as e:
        print(f"❌ {engine_name.upper()} ({key_id}) Failed: {e}")
        return None

def update_news_json(topic, excerpt, category, img_url):
    """Intercepts the JSON save and beams the summary to MongoDB!"""
    if articles_collection is not None:
        safe_id = "".join(x for x in topic if x.isalnum())[:20]
        new_article = {
            "title": topic,
            "excerpt": excerpt,
            "category": category,
            "readTime": "3 min read",
            "timestamp": time.time(), 
            "date": datetime.now().strftime("%b %d, %Y"),
            "imageUrl": img_url
        }
        articles_collection.update_one({"_id": safe_id}, {"$set": new_article}, upsert=True)
    else:
        print("⚠️ MONGO_URI missing! Cannot save to database.")

def generate_html_page(title, img_url, content):
    """Intercepts the HTML save and attaches the full article text to MongoDB!"""
    if articles_collection is not None:
        safe_id = "".join(x for x in title if x.isalnum())[:20]
        articles_collection.update_one({"_id": safe_id}, {"$set": {"full_content": content}}, upsert=True)

def delete_news_article(post_number):
    """Emergency kill-switch to delete a post from MongoDB."""
    if articles_collection is not None:
        try:
            recent_articles = list(articles_collection.find().sort("timestamp", -1).limit(int(post_number)))
            if len(recent_articles) >= int(post_number):
                target_article = recent_articles[-1]
                articles_collection.delete_one({"_id": target_article["_id"]})
                return target_article.get("title", "Unknown Title")
        except Exception as e:
            print(f"Error deleting: {e}")
    return None
