import os
import urllib.parse
import threading
import asyncio
from flask import Flask, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from brain import write_news_article, delete_news_article
from dotenv import load_dotenv

load_dotenv()

# --- THE LIVE NEWS API SERVER (Keeping it alive for health checks) ---
app_web = Flask(__name__)

@app_web.route('/')
def health_check():
    return "🤖 AI Writer Bot is Alive and Running!"

def run_web():
    app_web.run(host="0.0.0.0", port=8080)

# --- CORE PROCESSING LOGIC ---
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Original Talkative Logic + New Telegram Bridge Output."""
    document = update.message.document
    if not document.file_name.endswith('.txt'):
        return

    # 1. Talk back to the user (Original Logic)
    await update.message.reply_text("📥 Received Trends File! Starting Full Auto-Pilot...")
    
    file = await context.bot.get_file(document.file_id)
    file_path = "temp_trends.txt"
    await file.download_to_drive(file_path)
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
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
                
    # 2. Status Update (Original Logic)
    await update.message.reply_text(f"🤖 Extracted {len(topics)} topics. Passing to the Mega-Pool now...")

    success_count = 0
    for topic in topics:
        try:
            source_url = f"https://news.google.com/search?q={urllib.parse.quote(topic)}"
            # Write the article using brain.py
            content = write_news_article(source_url, topic)
            
            if not content:
                continue
            
            # 3. THE BRIDGE: Send the structured data back to Telegram for Bot #2
            # We use tags so the uploader bot knows exactly what is what
            report = (
                f"---NEW_ARTICLE_DATA---\n"
                f"TITLE: {topic}\n"
                f"IMAGE: https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=900\n" # Placeholder or logic from brain
                f"CONTENT: {content}\n"
                f"---END_DATA---"
            )
            await update.message.reply_text(report)
            success_count += 1
            
        except Exception as e:
            print(f"Failed on {topic}: {e}")
            
    if os.path.exists(file_path):
        os.remove(file_path)
        
    await update.message.reply_text(f"✅ Auto-Pilot Complete! {success_count} articles sent for upload.")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 PONG! Koyeb AI Writer is standing by.")

if __name__ == '__main__':
    threading.Thread(target=run_web, daemon=True).start()

    token = os.getenv("PUBLISHER_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    print("🚀 Koyeb Bot is Running...")
    app.run_polling(drop_pending_updates=True)
