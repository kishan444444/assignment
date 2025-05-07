📰 News Ingestion & SQL Query Pipeline (FastAPI + LangChain + Groq)
This project fetches real-time news articles from Bing News, stores them in a MySQL database, and allows you to query them using natural language through a LangChain agent powered by Groq's LLaMA3 model — all wrapped in a FastAPI web service.

🚀 Features
✅ Asynchronously scrapes top news related to a given topic.

✅ Stores article metadata into MySQL (documents table).

✅ Uses LangChain + Groq LLaMA3 to allow natural language querying of the news.

✅ Exposes everything via a FastAPI POST API endpoint.

✅ SQLite is used as the SQLDatabase for LangChain agent context (customizable).

📦 Requirements
Install all required dependencies:

bash
Copy
Edit
pip install fastapi uvicorn aiohttp aiomysql pymysql sqlite3 nest_asyncio beautifulsoup4 langchain langchain_groq
🛠 Configuration
Make sure your MySQL server is running and the documents table exists in a federal_data database:

sql
Copy
Edit
CREATE DATABASE IF NOT EXISTS federal_data;

USE federal_data;

CREATE TABLE IF NOT EXISTS documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    url TEXT,
    summary TEXT,
    published_date DATETIME,
    company_name TEXT
);
Update the credentials and file paths in the script:

python
Copy
Edit
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',
    'db': 'federal_data'
}

SQLITE_DB_PATH = 'federal_data.db'
GROQ_API_KEY = "your_groq_api_key"
LLAMA_MODEL_NAME = "Llama3-8b-8192"
🧠 How It Works
When /run-pipeline endpoint is triggered, it:

Scrapes Bing News for the topic (default: "OpenAI").

Saves article titles and URLs into the MySQL documents table.

Runs a SQL agent query ("give me list of all documents in table") using LangChain with Groq model.

📡 API Usage
Run the Server
bash
Copy
Edit
uvicorn main:app --reload
Trigger the Pipeline
bash
Copy
Edit
curl -X POST http://localhost:8000/run-pipeline
Response
json
Copy
Edit
{
  "status": "success",
  "message": "Agent Response: ..."
}
📁 Project Structure
bash
Copy
Edit
main.py          # FastAPI app and pipeline logic
federal_data.db  # SQLite DB used by LangChain (optional)
README.md
📋 TODO / Improvements
Add ability to change topic via API query param.

Add full-text search or keyword filtering.

Add user-facing front-end dashboard.

Replace SQLite with MySQL in LangChain if needed.

