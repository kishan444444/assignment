# 📰 News Data Pipeline with LLM-Powered SQL Agent

This project fetches the latest news articles related to a topic (default: **OpenAI**) from Bing News, stores the data in a MySQL database, and uses a LangChain + Groq LLM agent to query a local SQLite database. It is deployed as a FastAPI service.

## 🚀 Features

- 🔍 **Web Scraping**: Retrieves top news articles using `aiohttp` and `BeautifulSoup` from Bing News.
- 💾 **Async MySQL Storage**: Stores scraped article metadata in a MySQL database via `aiomysql`.
- 🤖 **LangChain Agent**: Uses `ChatGroq` LLM to interact with a SQL database using natural language queries.
- ⚡ **FastAPI API**: RESTful endpoints to run the pipeline and interact with the agent.

## 🏗️ Tech Stack

- **Python 3.10+**
- **FastAPI**
- **aiohttp** / **aiomysql**
- **BeautifulSoup**
- **LangChain + Groq (LLaMA3-8B-8192)**
- **MySQL + SQLite**

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/news-llm-pipeline.git
cd news-llm-pipeline
2. Create & Activate Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
3. Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
4. Configure Environment
Update database credentials and Groq API key in the main.py or config.py file:

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

GROQ_API_KEY = "your_groq_api_key"
5. Run FastAPI Server
bash
Copy
Edit
uvicorn main:app --reload
🔧 API Endpoints
GET /run-pipeline
Triggers the news fetch and database insertion pipeline.

Returns a success message with number of articles stored.

GET /query-agent?question=...
Accepts a natural language SQL query.

Returns the LLM-generated answer from the SQLite database.

🧪 Example Usage
http
Copy
Edit
GET /run-pipeline
http
Copy
Edit
GET /query-agent?question=List all documents in the table.
📁 Project Structure
graphql
Copy
Edit
.
├── main.py            # FastAPI app with endpoints
├── db_utils.py        # Async MySQL utilities
├── scraper.py         # News scraping logic
├── agent.py           # LangChain + Groq agent setup
├── federal_data.db    # SQLite DB used by agent
├── requirements.txt
└── README.md


