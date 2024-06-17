import unittest
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

class TestAgent(unittest.TestCase):
    def setUp(self):
        # Retrieve the AlphaVantage API key from the environment variable
        ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

        self.symbol_search = RexiaAIAlphaVantageSearchSymbols(api_key=ALPHA_VANTAGE_API_KEY)
        self.top_gainers_losers = RexiaAIAlphaVantageTopGainersLosers(api_key=ALPHA_VANTAGE_API_KEY)
        self.time_series_daily = RexiaAIAlphaVantageTimeSeriesDaily(api_key=ALPHA_VANTAGE_API_KEY)
        self.time_series_weekly = RexiaAIAlphaVantageTimeSeriesWeekly(api_key=ALPHA_VANTAGE_API_KEY)
        self.quote_endpoint = RexiaAIAlphaVantageQuoteEndpoint(api_key=ALPHA_VANTAGE_API_KEY)
        self.market_news_sentiment = RexiaAIAlphaVantageMarketNewsSentiment(api_key=ALPHA_VANTAGE_API_KEY)
        self.exchange_rate = RexiaAIAlphaVantageExchangeRate(api_key=ALPHA_VANTAGE_API_KEY)

        tools = {
            self.symbol_search.to_rexiaai_function_call()["name"]: self.symbol_search,
            self.top_gainers_losers.to_rexiaai_function_call()["name"]: self.top_gainers_losers,
            self.time_series_daily.to_rexiaai_function_call()["name"]: self.time_series_daily,
            self.time_series_weekly.to_rexiaai_function_call()["name"]: self.time_series_weekly,
            self.quote_endpoint.to_rexiaai_function_call()["name"]: self.quote_endpoint,
            self.market_news_sentiment.to_rexiaai_function_call()["name"]: self.market_news_sentiment,
            self.exchange_rate.to_rexiaai_function_call()["name"]: self.exchange_rate,
        }

        self.llm = RexiaAIOpenAI(
            base_url="http://localhost:1234/v1",
            model="lm-studio-server",
            temperature=0,
            tools=tools,
        )

        self.agent = Agent(
            llm=self.llm,
            task="Give me a report on NVIDIA's (Stock Symbol NASDAQ: NVDA) performance this week, including market sentiment.",
            verbose=True,
        )

    def test_response_format(self):
        response = self.agent.reflect()

        self.assertIsInstance(response, dict)
        expected_keys = ['question', 'answer', 'confidence_score', 'chain_of_reasoning']
        self.assertEqual(set(response.keys()), set(expected_keys))

if __name__ == '__main__':
    unittest.main()