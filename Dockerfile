# 1. Start with a standard Python 3.13 environment
FROM python:3.13-slim

# 2. Set up our working folder
WORKDIR /app

# 3. Copy your requirements and install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy all your files into the server
COPY . .

# 5. Open the port Koyeb needs for the Flask health check
EXPOSE 8080

# 6. Run ONLY the Python bot
CMD ["python3", "bot_manager.py"]
