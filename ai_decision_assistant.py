import openai
import sqlite3
import requests
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Initialize SQLite Database (for storing queries & responses)
conn = sqlite3.connect("business_ai.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    response TEXT
)
""")
conn.commit()

# API Keys
OPENAI_API_KEY = "your-api-key"
ALPHA_VANTAGE_API_KEY = "your-alpha-vantage-key"
NEWS_API_KEY = "your-news-api-key"

openai.api_key = OPENAI_API_KEY


def get_financial_data(symbol):
    """Fetches real-time stock or market data from Alpha Vantage."""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("Time Series (5min)", {})
    return "No financial data available."


def get_news_data(query):
    """Fetches latest news articles relevant to the business query."""
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        return [article["title"] for article in articles[:5]]
    return "No relevant news found."


def get_ai_response(user_query):
    """Generates AI-driven business recommendations incorporating financial and market insights."""
    words = user_query.split()
    stock_symbol = next((word for word in words if word.isupper() and len(word) <= 5), None)
    financial_data = get_financial_data(stock_symbol) if stock_symbol else ""
    news_data = get_news_data(user_query)
    
    prompt = f"""You are a business strategy AI. Answer the following question with a structured, data-driven approach:
    {user_query}
    
    Financial Data (if applicable): {financial_data}
    
    Latest Market News: {news_data}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI business consultant."},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_query = data.get("query")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    
    ai_response = get_ai_response(user_query)
    
    cursor.execute("INSERT INTO queries (query, response) VALUES (?, ?)", (user_query, ai_response))
    conn.commit()
    
    return jsonify({"query": user_query, "response": ai_response})

if __name__ == "__main__":
    app.run(debug=True)
