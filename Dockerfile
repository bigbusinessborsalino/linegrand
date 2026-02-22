# 1. Start with a standard Python 3.13 environment
FROM python:3.13-slim

# 2. Install Node.js (version 20) and npm directly into the OS
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs

# 3. Set up our working folder
WORKDIR /app

# 4. Copy your requirements and install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy all your files into the server
COPY . .

# 6. Install Node dependencies and build the React site
RUN npm install
RUN npm run build

# 7. Open the port Koyeb needs for the health check
EXPOSE 8080

# 8. Run your hybrid start command
CMD ["npm", "run", "start"]
