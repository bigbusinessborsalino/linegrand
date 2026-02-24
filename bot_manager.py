import os
import json
import urllib.parse
import threading
from flask import Flask, jsonify, send_from_directory
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from brain import write_news_article, update_news_json, generate_html_page, delete_news_article
from dotenv import load_dotenv

load_dotenv()

# --- THE LIVE NEWS API SERVER (THE BRIDGE) ---
app_web = Flask(__name__)

@app_web.route('/')
def health_check():
    return "🤖 AI Writer Bot is Alive and Running!"

# 1. This endpoint sends your news.json directly to your Render website
@app_web.route('/api/news')
def get_live_news():
    try:
        with open('public/news.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        response = jsonify(data)
    except Exception:
        response = jsonify([]) # Returns empty if no news exists yet
        
    # Security bypass: Allows your Render domain to read this data safely
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# 2. This endpoint exposes your HTML articles to the internet
@app_web.route('/<path:filename>')
def serve_html_articles(filename):
    return send_from_directory('public', filename)

def run_web():
    # Running on 0.0.0.0 allows Koyeb to ping it from outside
    app_web.run(host="0.0.0.0", port=8080)
# ----------------------------

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Intercepts the .txt file and Auto-Publishes the Highest and Lowest story per region."""
    document = update.message.document
    
    if not document.file_name.endswith('.txt'):
        return

    await update.message.reply_text("📥 Received Trends File! Starting Full Auto-Pilot...")
    
    # Download the file to read it
    file = await context.bot.get_file(document.file_id)
    file_path = "temp_trends.txt"
    await file.download_to_drive(file_path)
    
    # Read the topics
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    final_topics = []
    current_country_topics = []
    
    for line in lines:
        if line.startswith("--- NEW TRENDS IN"):
            # If we just finished a country, extract its Highest (First) and Lowest (Last)
            if current_country_topics:
                if len(current_country_topics) >= 2:
                    final_topics.append(current_country_topics[0])  
                    final_topics.append(current_country_topics[-1]) 
                else:
                    final_topics.append(current_country_topics[0])
            
            # Reset the list for the new country we just hit
            current_country_topics = [] 
            
        elif line.startswith("Topic:"):
            topic = line.split("Topic:")[1].split("(")[0].strip()
            if topic not in current_country_topics:
                current_country_topics.append(topic)
                
    # Process the very last country in the text file
    if current_country_topics:
        if len(current_country_topics) >= 2:
            final_topics.append(current_country_topics[0])
            final_topics.append(current_country_topics[-1])
        else:
            final_topics.append(current_country_topics[0])

    # Remove any duplicate topics across different countries to save API calls
    topics = []
    for t in final_topics:
        if t not in topics:
            topics.append(t)
                
    await update.message.reply_text(f"🤖 Extracted {len(topics)} topics (Highest & Lowest from each region). Passing to the Mega-Pool now...")

    success_count = 0
    for topic in topics:
        try:
            # 1. AI writes the article
            source_url = f"https://news.google.com/search?q={urllib.parse.quote(topic)}"
            content = write_news_article(source_url, topic)
            
            if not content:
                continue
                
            # 2. Publish to React UI and HTML (Passing empty strings instead of images)
            update_news_json(topic, content[:150] + "...", "Trending", "")
            generate_html_page(topic, "", content)
            
            success_count += 1
            print(f"Published Text Only: {topic}")
        except Exception as e:
            print(f"Failed on {topic}: {e}")
            
    # Clean up the text file
    if os.path.exists(file_path):
        os.remove(file_path)
        
    await update.message.reply_text(f"✅ Auto-Pilot Complete! Published {success_count} text articles.")

async def delete_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Emergency kill-switch to delete a post."""
    try:
        post_number = context.args[0]
        deleted_title = delete_news_article(post_number)
        
        if deleted_title:
            await update.message.reply_text(f"🗑️ Successfully deleted: {deleted_title}")
        else:
            await update.message.reply_text("❌ Could not find that post number. Check your news.json.")
    except IndexError:
        await update.message.reply_text("Usage: /delete <number>\nExample: /delete 1 (deletes the newest post)")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simple ping-pong to test if the bot is alive."""
    await update.message.reply_text("🏓 PONG! Publisher Bot is alive and well.")

if __name__ == '__main__':
    # 1. Start the Live News API Server in the background
    print("🌐 Starting Live News API Server for Koyeb & Render...")
    threading.Thread(target=run_web, daemon=True).start()

    # 2. Start the Telegram Bot setup
    token = os.getenv("PUBLISHER_BOT_TOKEN")
    
    app = (
        ApplicationBuilder()
        .token(token)
        .connect_timeout(60) 
        .read_timeout(60)
        .write_timeout(60)
        .pool_timeout(60)
        .build()
    )
    
    # Add Handlers
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("delete", delete_post))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    print("🚀 Attempting to connect to Telegram... (This might take a minute)")
    
    try:
        app.run_polling(drop_pending_updates=True, close_loop=False)
    except Exception as e:
        print(f"❌ DEADLY ERROR: {e}")
