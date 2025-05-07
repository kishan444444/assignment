import aiohttp
import asyncio
import aiomysql
import sqlite3
import pymysql
import nest_asyncio
import logging
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from langchain_groq import ChatGroq
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase
from langchain.agents import AgentExecutor
from fastapi import FastAPI
import uvicorn

# ---- Configuration Constants ----
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'verms9425604852',
    'db': 'federal_data'
}

SQLITE_DB_PATH = 'federal_data.db'
GROQ_API_KEY = "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"
LLAMA_MODEL_NAME = "Llama3-8b-8192"

# ---- Logger Setup ----
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---- FastAPI Setup ----
app = FastAPI()

# ---- Database Utility Functions ----

async def get_mysql_connection():
    """Create and return an async MySQL connection."""
    try:
        return await aiomysql.connect(**DB_CONFIG)
    except Exception as e:
        logger.error(f"Error establishing MySQL connection: {e}")
        raise

async def save_to_mysql(docs):
    """Save fetched documents to MySQL."""
    conn = await get_mysql_connection()
    async with conn.cursor() as cur:
        for doc in docs:
            try:
                summary = "Summary not available"
                published_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                company_name = "Company not available"
                
                # Prepare and execute insert query
                await cur.execute(""" 
                    INSERT INTO documents (title, url, summary, published_date, company_name)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    doc.get('title'),
                    doc.get('url'),
                    summary,
                    published_date,
                    company_name
                ))
            except Exception as e:
                logger.error(f"Error inserting document: {e}")
        await conn.commit()
        conn.close()

# ---- Web Scraping Utility Functions ----

async def fetch_documents(topic="OpenAI", max_articles=10):
    """Fetch top news articles related to a given topic from Bing News."""
    search_url = f"https://www.bing.com/news/search?q={topic.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    articles = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, headers=headers) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                base_url = "https://www.bing.com"

                for link in soup.find_all("a", href=True):
                    url = urljoin(base_url, link["href"])
                    title = link.get_text(strip=True)

                    if (
                        url.startswith("http")
                        and "bing.com" not in url
                        and title
                        and len(title) > 15
                    ):
                        articles.append({"title": title, "url": url})

                    if len(articles) >= max_articles:
                        break
        logger.info(f"✅ Fetched {len(articles)} articles.")
        return articles
    except Exception as e:
        logger.error(f"❌ Error fetching news: {e}")
        return []

# ---- LangChain Agent Setup ----

def setup_langchain_agent():
    """Set up the LangChain agent with SQLite database and Groq model."""
    sqlite_connection = sqlite3.connect(SQLITE_DB_PATH)
    db = SQLDatabase.from_uri(f"sqlite:///{SQLITE_DB_PATH}")

    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name=LLAMA_MODEL_NAME, streaming=True)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # Create the agent and the AgentExecutor
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )
    
    agent_executor = AgentExecutor(agent=agent, tools=[toolkit], verbose=True)

    return agent_executor

# ---- FastAPI Endpoint to Trigger Pipeline ----

@app.post("/run-pipeline")
async def run_pipeline():
    """Endpoint to trigger the main pipeline to fetch, save, and process documents."""
    logger.info("🚀 Starting pipeline...")
    docs = await fetch_documents()
    if docs:
        await save_to_mysql(docs)
        logger.info("✅ Saved documents to MySQL.")

        # Set up the agent and run query
        agent_executor = setup_langchain_agent()
        query = "give me list of all documents in table"
        response = await agent_executor.arun(query)  # Ensure async execution
        logger.info(f"Agent Response: {response}")
        return {"status": "success", "message": f"Agent Response: {response}"}
    else:
        logger.warning("No documents fetched. Skipping further processing.")
        return {"status": "failure", "message": "No documents fetched."}

# ---- FastAPI Server Execution ----
nest_asyncio.apply()

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
