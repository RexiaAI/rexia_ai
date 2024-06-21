"""Example symbol searching with ReXia.AI AlphaVantage tool. You need an alpha vantage api key to use it."""

# Import necessary modules
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.tools import (
    RexiaAIAlphaVantageTopGainersLosers,
    RexiaAIAlphaVantageSearchSymbols,
    RexiaAIAlphaVantageTimeSeriesDaily,
    RexiaAIAlphaVantageTimeSeriesWeekly,
    RexiaAIAlphaVantageQuoteEndpoint,
    RexiaAIAlphaVantageMarketNewsSentiment,
    RexiaAIAlphaVantageExchangeRate,
)

# Retrieve the AlphaVantage API key from the environment variable
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")

# Create instances of the AlphaVantage tools
symbol_search = RexiaAIAlphaVantageSearchSymbols(api_key=ALPHA_VANTAGE_API_KEY)
top_gainers_losers = RexiaAIAlphaVantageTopGainersLosers(api_key=ALPHA_VANTAGE_API_KEY)
time_series_daily = RexiaAIAlphaVantageTimeSeriesDaily(api_key=ALPHA_VANTAGE_API_KEY)
time_series_weekly = RexiaAIAlphaVantageTimeSeriesWeekly(api_key=ALPHA_VANTAGE_API_KEY)
quote_endpoint = RexiaAIAlphaVantageQuoteEndpoint(api_key=ALPHA_VANTAGE_API_KEY)
market_news_sentiment = RexiaAIAlphaVantageMarketNewsSentiment(
    api_key=ALPHA_VANTAGE_API_KEY
)
exchange_rate = RexiaAIAlphaVantageExchangeRate(api_key=ALPHA_VANTAGE_API_KEY)

# Create a dictionary mapping tool names to their instances
tools = {
    symbol_search.to_rexiaai_function_call()["name"]: symbol_search,
    top_gainers_losers.to_rexiaai_function_call()["name"]: top_gainers_losers,
    time_series_daily.to_rexiaai_function_call()["name"]: time_series_daily,
    time_series_weekly.to_rexiaai_function_call()["name"]: time_series_weekly,
    quote_endpoint.to_rexiaai_function_call()["name"]: quote_endpoint,
    market_news_sentiment.to_rexiaai_function_call()["name"]: market_news_sentiment,
    exchange_rate.to_rexiaai_function_call()["name"]: exchange_rate,
}

# Create an instance of the RexiaAI LLM
llm = RexiaAIOpenAI(
    base_url="https://api.01.ai/v1",
    model="yi-large",
    temperature=0,
    api_key=YI_LARGE_API_KEY,
    tools=tools,
    max_tokens=4000,
)

# Create an instance of the RexiaAI Agent with the specified task and LLM
agent = Agent(
    llm=llm,
    task="What is the stock price for NVIDIA (Stock Symbol NASDAQ: NVDA).",
    verbose=True,
)

api_result = quote_endpoint.get_quote_endpoint(symbol="NVDA")

# Generate the response from the agent
response = agent.reflect()

# Print the response
print("Response:", response)

print("API Result:", api_result)
