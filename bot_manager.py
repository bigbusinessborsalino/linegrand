import os
import urllib.parse
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
# Notice the new get_pexels_image import at the end of this line!
from brain import write_news_article, update_news_json, generate_html_page, delete_news_article, get_pexels_image
from dotenv import load_dotenv

load_dotenv()

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Intercepts the .txt file and Auto-Publishes up to 20 stories."""
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
        
    topics = []
    for line in lines:
        if line.startswith("Topic:"):
            # Extract just the topic name (ignoring the search count)
            topic = line.split("Topic:")[1].split("(")[0].strip()
            if topic not in topics:
                topics.append(topic)
                
    # Limit to top 4 topics for testing (we will change this to 20 later!)
    topics = topics[:4]
    await update.message.reply_text(f"🤖 Extracted {len(topics)} topics. Writing articles and fetching photos now...")

    success_count = 0
    for topic in topics:
        try:
            # 1. AI writes the article
            source_url = f"https://news.google.com/search?q={urllib.parse.quote(topic)}"
            content = write_news_article(source_url, topic)
            
            if not content:
                continue
                
            # 2. Get the REAL copyright-free photograph from Pexels
            img_url = get_pexels_image(topic)
            
            # 3. Publish to React UI and HTML
            update_news_json(topic, content[:150] + "...", "Trending", img_url)
            generate_html_page(topic, img_url, content)
            
            success_count += 1
            print(f"Published: {topic}")
        except Exception as e:
            print(f"Failed on {topic}: {e}")
            
    # Clean up the text file
    if os.path.exists(file_path):
        os.remove(file_path)
        
    await update.message.reply_text(f"✅ Auto-Pilot Complete! Published {success_count} new articles. Refresh grandlinenews.com!")

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
    token = os.getenv("PUBLISHER_BOT_TOKEN")
    
    # We are building the app with massive timeouts and a connection pool
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
    app.add_handler(CommandHandler("ping", ping)) # <--- NEW PING COMMAND
    app.add_handler(CommandHandler("delete", delete_post))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    print("🚀 Attempting to connect to Telegram... (This might take a minute)")
    
    try:
        # 'drop_pending_updates' cleans out the 'stuck' messages from the last crash
        app.run_polling(drop_pending_updates=True, close_loop=False)
    except Exception as e:
        print(f"❌ DEADLY ERROR: {e}")
