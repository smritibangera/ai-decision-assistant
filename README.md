# AI-Powered Strategic Decision-Making Assistant 🚀

This project is an AI-driven assistant that provides **real-time business strategy recommendations** based on financial data and market news.

## Features:
- Integrates **GPT-4** for business insights.
- Fetches **real-time stock market data** using Alpha Vantage API.
- Retrieves **latest market news** for relevant trends.
- Provides AI-driven **scenario-based decision-making**.

## Setup & Installation:
1. Clone the repo: git clone https://github.com/your-username/ai-decision-assistant.git cd ai-decision-assistant

2. Install dependencies: pip install flask openai requests sqlite3

3. Run the API: python ai_decision_assistant.py


## API Usage:
- Send a **POST request** to `/ask` with a business-related query.
- Example request:
```json
{ "query": "Should we expand into the US market?" }

The AI assistant will return data-driven insights.

Authors:
Smriti (@your-github)
License:
This project is licensed under MIT License.


