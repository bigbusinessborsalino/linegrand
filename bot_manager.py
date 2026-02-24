import os
import urllib.parse
import threading
from flask import Flask, jsonify, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from pymongo import MongoClient
from brain import write_news_article, delete_news_article
from dotenv import load_dotenv

load_dotenv()

# --- MONGODB SETUP FOR THE API ---
MONGO_URI = os.getenv("MONGO_URI")
db_client = MongoClient(MONGO_URI) if MONGO_URI is not None else None
db = db_client.grandline_news if db_client is not None else None
articles_collection = db.articles if db is not None else None

# --- THE LIVE NEWS API SERVER (THE BRIDGE) ---
app_web = Flask(__name__)

@app_web.route('/')
def health_check():
    return "🤖 AI Writer Bot is Alive and Running!"

@app_web.route('/api/news')
def get_live_news():
    if articles_collection is not None:
        articles = list(articles_collection.find({}, {"_id": 0}).sort("timestamp", -1))
        response = jsonify(articles)
    else:
        response = jsonify([])
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# 🚀 NEW: THE SECRET DOOR FOR YOUR BROADCASTER!
@app_web.route('/api/trigger-writer', methods=['POST'])
def trigger_writer():
    data = request.json
    if not data or 'raw_text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    raw_text = data['raw_text']
    
    # We run this in the background so Render doesn't have to wait 30 minutes for Koyeb to finish writing
    threading.Thread(target=process_raw_trends, args=(raw_text,), daemon=True).start()
    
    return jsonify({"message": "✅ Trends received! Mega-Pool is starting..."}), 200

def run_web():
    app_web.run(host="0.0.0.0", port=8080)
# ----------------------------


# --- CORE TOPIC PARSING LOGIC ---
def process_raw_trends(raw_text):
    print("📥 Processing Trends! Starting Full Auto-Pilot...")
    lines = raw_text.split('\n')
    
    final_topics = []
    current_country_topics = []
    
    for line in lines:
        if line.startswith("--- NEW TRENDS IN"):
            if current_country_topics:
                if len(current_country_topics) >= 2:
                    final_topics.append(current_country_topics[0])  
                    final_topics.append(current_country_topics[-1]) 
                else:
                    final_topics.append(current_country_topics[0])
            current_country_topics = [] 
            
        elif line.startswith("Topic:"):
            topic = line.split("Topic:")[1].split("(")[0].strip()
            if topic not in current_country_topics:
                current_country_topics.append(topic)
                
    if current_country_topics:
        if len(current_country_topics) >= 2:
            final_topics.append(current_country_topics[0])
            final_topics.append(current_country_topics[-1])
        else:
            final_topics.append(current_country_topics[0])

    topics = []
    for t in final_topics:
        if t not in topics:
            topics.append(t)
                
    print(f"🤖 Extracted {len(topics)} topics. Passing to the Mega-Pool now...")

    success_count = 0
    for topic in topics:
        try:
            source_url = f"https://news.google.com/search?q={urllib.parse.quote(topic)}"
            content = write_news_article(source_url, topic)
            if not content:
                continue
            success_count += 1
            print(f"Published to MongoDB: {topic}")
        except Exception as e:
            print(f"Failed on {topic}: {e}")
            
    print(f"✅ Auto-Pilot Complete! Saved {success_count} articles to the cloud database.")


# --- TELEGRAM COMMANDS ---
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Still allows YOU to manually upload files via Telegram for testing."""
    document = update.message.document
    if not document.file_name.endswith('.txt'):
        return

    await update.message.reply_text("📥 Received Trends File manually! Starting...")
    
    file = await context.bot.get_file(document.file_id)
    file_path = "temp_trends.txt"
    await file.download_to_drive(file_path)
    
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
        
    if os.path.exists(file_path):
        os.remove(file_path)

    threading.Thread(target=process_raw_trends, args=(raw_text,), daemon=True).start()
    await update.message.reply_text("✅ Trends sent to background worker. Check Koyeb logs!")

async def delete_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        post_number = context.args[0]
        deleted_title = delete_news_article(post_number)
        if deleted_title:
            await update.message.reply_text(f"🗑️ Successfully deleted: {deleted_title}")
        else:
            await update.message.reply_text("❌ Could not find that post number in MongoDB.")
    except IndexError:
        await update.message.reply_text("Usage: /delete <number>\nExample: /delete 1 (deletes the newest post)")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 PONG! Publisher Bot is alive and well.")

if __name__ == '__main__':
    print("🌐 Starting Live News API Server for Koyeb & Render...")
    threading.Thread(target=run_web, daemon=True).start()

    token = os.getenv("PUBLISHER_BOT_TOKEN")
    app = ApplicationBuilder().token(token).connect_timeout(60).read_timeout(60).write_timeout(60).pool_timeout(60).build()
    
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("delete", delete_post))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    print("🚀 Attempting to connect to Telegram...")
    try:
        app.run_polling(drop_pending_updates=True, close_loop=False)
    except Exception as e:
        print(f"❌ DEADLY ERROR: {e}")
