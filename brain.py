import os
import requests
import itertools
import json
from datetime import datetime
from google import genai
from groq import Groq
import time 
import cohere
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize All 4 AI Engines (Updated to the new Google GenAI standard)
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
or_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# 2. The Load Balancer
engine_cycle = itertools.cycle(["gemini", "groq", "cohere", "openrouter"])

import time # <--- Add this at the top of the file with the other imports if it isn't there!

def write_news_article(source_url, topic):
    """Writes an article using the next available AI engine."""
    current_engine = next(engine_cycle)
    print(f"🧠 Brain Selected: {current_engine.upper()}")
    
    # Give the free APIs a tiny 5-second breath so they don't panic
    time.sleep(5) 
    
    prompt = f"Write a 300-word exciting news article about {topic}. Be professional but engaging. Format in clean paragraphs, no markdown."
    
    try:
        if current_engine == "gemini":
            response = gemini_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text
            
        elif current_engine == "groq":
            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant", # <--- UPDATED GROQ MODEL
                messages=[{"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content
            
        elif current_engine == "cohere":
            response = cohere_client.chat(message=prompt)
            return response.text
            
        elif current_engine == "openrouter":
            completion = or_client.chat.completions.create(
                model="meta-llama/llama-3.3-70b-instruct:free", # <--- UPDATED OPENROUTER MODEL
                messages=[{"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content
            
    except Exception as e:
        print(f"❌ {current_engine.upper()} Failed: {e}")
        return None

def update_news_json(topic, excerpt, category, img_url):
    """Saves the article to the React database."""
    safe_name = "".join(x for x in topic if x.isalnum())[:20]
    filepath = "public/news.json"
    
    new_article = {
        "id": safe_name,
        "title": topic,
        "excerpt": excerpt,
        "category": category,
        "readTime": "3 min read",
        "date": datetime.now().strftime("%b %d, %Y"),
        "imageUrl": img_url
    }
    
    articles = []
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                articles = json.load(f)
            except:
                pass
                
    # Insert at the top so it appears first on the website
    articles.insert(0, new_article)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4)

def generate_html_page(title, img_url, content):
    """Generates a standalone HTML page with Related News."""
    safe_name = "".join(x for x in title if x.isalnum())[:20]
    filename = f"public/{safe_name}.html"
    
    paragraphs = "".join([f"<p style='margin-bottom: 1.5rem; line-height: 1.8; color: #374151;'>{p.strip()}</p>" for p in content.split('\n') if p.strip()])
    fallback_img = "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=900&q=80"
    
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
                <img src="{img_url}" alt="{title}" class="w-full h-[400px] object-cover" onerror="this.src='{fallback_img}'" />
                <div class="p-8 md:p-12">
                    <h1 class="text-3xl md:text-5xl font-black leading-tight mb-8">{title}</h1>
                    <div class="text-lg md:text-xl">
                        {paragraphs}
                    </div>
                </div>
            </article>
            <div>
                <div class="flex items-center gap-3 mb-6">
                    <div class="w-1.5 h-6 bg-red-700 rounded-full"></div>
                    <h2 class="text-2xl font-bold">Related Stories</h2>
                </div>
                <div id="related-news" class="grid grid-cols-1 md:grid-cols-3 gap-6"></div>
            </div>
        </main>
        <footer class="bg-white border-t border-gray-200 text-center py-8 text-gray-500 text-sm">
            &copy; 2026 Grand Line News | Automated by Reigen
        </footer>
        <script>
            fetch('/news.json')
                .then(res => res.json())
                .then(articles => {{
                    const others = articles.filter(a => a.title !== "{title}");
                    const shuffled = others.sort(() => 0.5 - Math.random());
                    const selected = shuffled.slice(0, 3);
                    const container = document.getElementById('related-news');
                    selected.forEach(article => {{
                        const safeName = article.title.replace(/[^a-zA-Z0-9]/g, '').substring(0, 20);
                        const link = '/' + safeName + '.html';
                        const img = article.imageUrl || article.image || '{fallback_img}';
                        let cardHTML = '<a href="' + link + '" class="group flex flex-col bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden transition-all hover:shadow-md hover:-translate-y-1">';
                        cardHTML += '<img src="' + img + '" class="w-full h-48 object-cover" onerror="this.src=\'{fallback_img}\'" />';
                        cardHTML += '<div class="p-5 flex-1 flex flex-col">';
                        cardHTML += '<span class="text-xs font-bold text-red-700 uppercase mb-2">' + (article.category || 'Trending') + '</span>';
                        cardHTML += '<h3 class="font-bold text-gray-900 leading-snug line-clamp-3 group-hover:text-red-700 transition-colors">' + article.title + '</h3>';
                        cardHTML += '</div></a>';
                        container.innerHTML += cardHTML;
                    }});
                }})
                .catch(err => console.error(err));
        </script>
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


def get_pexels_image(query):
    """Fetches high-quality photos with a smart fallback system."""
    api_key = os.getenv("PEXELS_API_KEY")
    fallback_img = "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=900&q=80"
    
    if not api_key:
        return fallback_img
        
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": api_key}
    
    # Try 1: The specific topic (e.g., "lafc vs inter miami")
    # Try 2: A broader category as a fallback
    search_attempts = [query, "sports", "technology", "news"]
    
    for attempt in search_attempts:
        params = {"query": attempt, "per_page": 1, "orientation": "landscape"}
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("photos"):
                    print(f"📸 Pexels found image for: {attempt}")
                    return data["photos"][0]["src"]["landscape"]
        except Exception as e:
            print(f"⚠️ Pexels Error on {attempt}: {e}")
            continue
            
    return fallback_img
