import os
import requests
import itertools
import json
import time
from datetime import datetime
from google import genai
from groq import Groq
import cohere
from dotenv import load_dotenv

load_dotenv()

# --- 1. AUTO-DISCOVERY LOAD BALANCER ---
available_clients = []

# Scan the server for ANY numbered API keys and add them to the mega-pool
for key, value in os.environ.items():
    if key.startswith("GEMINI_API_KEY_") and value.strip():
        try:
            client = genai.Client(api_key=value.strip())
            available_clients.append({"engine": "gemini", "client": client, "key_id": key})
        except Exception as e:
            print(f"Failed to load {key}: {e}")

    elif key.startswith("GROQ_API_KEY_") and value.strip():
        try:
            client = Groq(api_key=value.strip())
            available_clients.append({"engine": "groq", "client": client, "key_id": key})
        except Exception as e:
            print(f"Failed to load {key}: {e}")

    elif key.startswith("COHERE_API_KEY_") and value.strip():
        try:
            client = cohere.Client(value.strip())
            available_clients.append({"engine": "cohere", "client": client, "key_id": key})
        except Exception as e:
            print(f"Failed to load {key}: {e}")

# Fallback just in case you test locally with the old un-numbered keys
if not available_clients:
    print("⚠️ No numbered keys found! Trying default un-numbered keys...")
    if os.getenv("GEMINI_API_KEY"):
        available_clients.append({"engine": "gemini", "client": genai.Client(api_key=os.getenv("GEMINI_API_KEY")), "key_id": "DEFAULT_GEMINI"})
    if os.getenv("GROQ_API_KEY"):
        available_clients.append({"engine": "groq", "client": Groq(api_key=os.getenv("GROQ_API_KEY")), "key_id": "DEFAULT_GROQ"})

if not available_clients:
    print("❌ CRITICAL ERROR: NO API KEYS FOUND AT ALL! The bot cannot write.")

# 2. Create the Infinite Cycle out of all 30+ keys
engine_cycle = itertools.cycle(available_clients)
print(f"🚀 MEGA-POOL INITIALIZED: {len(available_clients)} AI Engines loaded and ready!")

# --- 3. CORE BOT LOGIC ---

def write_news_article(source_url, topic):
    """Writes an article using the next available AI engine in the 30-key pool."""
    worker = next(engine_cycle)
    engine_name = worker["engine"]
    client = worker["client"]
    key_id = worker["key_id"]
    
    # This will print exactly which key is being used (e.g., "Using GEMINI_API_KEY_4")
    print(f"🧠 Brain Selected: {engine_name.upper()} (Powered by {key_id})")
    
    # A tiny breath to keep the servers happy
    time.sleep(2) 
    
    prompt = f"Write a 300-word exciting news article about {topic}. Be professional but engaging. Format in clean paragraphs, no markdown."
    
    try:
        if engine_name == "gemini":
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
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
    """Saves the article to the React database (Text Only)."""
    safe_name = "".join(x for x in topic if x.isalnum())[:20]
    filepath = "public/news.json"
    
    new_article = {
        "id": safe_name,
        "title": topic,
        "excerpt": excerpt,
        "category": category,
        "readTime": "3 min read",
        "date": datetime.now().strftime("%b %d, %Y"),
        "imageUrl": img_url # Will be empty based on bot_manager
    }
    
    articles = []
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                articles = json.load(f)
            except:
                pass
                
    articles.insert(0, new_article)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4)

def generate_html_page(title, img_url, content):
    """Generates a standalone HTML page (Text Only optimized)."""
    safe_name = "".join(x for x in title if x.isalnum())[:20]
    filename = f"public/{safe_name}.html"
    
    paragraphs = "".join([f"<p style='margin-bottom: 1.5rem; line-height: 1.8; color: #374151;'>{p.strip()}</p>" for p in content.split('\n') if p.strip()])
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} | Grand Line News</title>
        <link rel="icon" type="image/svg+xml" href="/logo.svg" />
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50 text-gray-900 font-sans">
        <nav class="bg-white shadow-sm py-4 px-6 mb-8">
            <div class="max-w-5xl mx-auto flex items-center">
                <a href="/" class="flex items-center gap-2 text-2xl font-black tracking-tight text-gray-900">
                    <img src="/logo.svg" alt="Logo" class="w-8 h-8" />
                    Grand Line News
                </a>
            </div>
        </nav>
        <main class="max-w-5xl mx-auto px-4 pb-12">
            <article class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden mb-12">
                <div class="p-8 md:p-12">
                    <h1 class="text-3xl md:text-5xl font-black leading-tight mb-8">{title}</h1>
                    <div class="text-lg md:text-xl">
                        {paragraphs}
                    </div>
                </div>
            </article>
        </main>
        <footer class="bg-white border-t border-gray-200 text-center py-8 text-gray-500 text-sm">
            &copy; 2026 Grand Line News | Automated by Reigen
        </footer>
    </body>
    </html>
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

def delete_news_article(post_number):
    """Emergency kill-switch to delete a post."""
    filepath = "public/news.json"
    if not os.path.exists(filepath): return None
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            articles = json.load(f)
        except: return None
    try:
        index = int(post_number) - 1
        deleted = articles.pop(index)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=4)
        html_path = f"public/{deleted['id']}.html"
        if os.path.exists(html_path): os.remove(html_path)
        return deleted["title"]
    except: return None
