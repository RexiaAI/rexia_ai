import unittest
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.structure import RexiaAIResponse
from verification.llm_verification import LLMVerification
from rexia_ai.tools import (
    RexiaAIAlphaVantageTopGainersLosers,
    RexiaAIAlphaVantageSearchSymbols,
    RexiaAIAlphaVantageTimeSeriesDaily,
    RexiaAIAlphaVantageTimeSeriesWeekly,
    RexiaAIAlphaVantageQuoteEndpoint,
    RexiaAIAlphaVantageMarketNewsSentiment,
    RexiaAIAlphaVantageExchangeRate,
)

class TestAlphaVantageTools(unittest.TestCase):
    def setUp(self):
        ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
        YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")
        BASE_URL = "https://api.01.ai/v1"
        
        if not ALPHA_VANTAGE_API_KEY:
            self.skipTest("AlphaVantage API key not found in environment variables.")

        if not os.getenv("YI_LARGE_API_KEY"):
            self.skipTest("YI_LARGE_API_KEY not found in environment variables.")

        self.symbol_search = RexiaAIAlphaVantageSearchSymbols(
            api_key=ALPHA_VANTAGE_API_KEY
        )
        self.top_gainers_losers = RexiaAIAlphaVantageTopGainersLosers(
            api_key=ALPHA_VANTAGE_API_KEY
        )
        self.time_series_daily = RexiaAIAlphaVantageTimeSeriesDaily(
            api_key=ALPHA_VANTAGE_API_KEY
        )
        self.time_series_weekly = RexiaAIAlphaVantageTimeSeriesWeekly(
            api_key=ALPHA_VANTAGE_API_KEY
        )
        self.quote_endpoint = RexiaAIAlphaVantageQuoteEndpoint(
            api_key=ALPHA_VANTAGE_API_KEY
        )
        self.market_news_sentiment = RexiaAIAlphaVantageMarketNewsSentiment(
            api_key=ALPHA_VANTAGE_API_KEY
        )
        self.exchange_rate = RexiaAIAlphaVantageExchangeRate(
            api_key=ALPHA_VANTAGE_API_KEY
        )

        tools = {
            self.symbol_search.to_rexiaai_function_call()["name"]: self.symbol_search,
            self.top_gainers_losers.to_rexiaai_function_call()[
                "name"
            ]: self.top_gainers_losers,
            self.time_series_daily.to_rexiaai_function_call()[
                "name"
            ]: self.time_series_daily,
            self.time_series_weekly.to_rexiaai_function_call()[
                "name"
            ]: self.time_series_weekly,
            self.quote_endpoint.to_rexiaai_function_call()["name"]: self.quote_endpoint,
            self.market_news_sentiment.to_rexiaai_function_call()[
                "name"
            ]: self.market_news_sentiment,
            self.exchange_rate.to_rexiaai_function_call()["name"]: self.exchange_rate,
        }

        self.llm = RexiaAIOpenAI(
            base_url=BASE_URL,
            model="yi-large",
            temperature=0,
            api_key=YI_LARGE_API_KEY,
            tools=tools,
        )
        
        self.llm_verification = LLMVerification(
            base_url=BASE_URL, 
            api_key=YI_LARGE_API_KEY,
            model="yi-large",
            temperature=0.0
        )

        self.agent = Agent(
            llm=self.llm,
            task="What is the stock price for NVIDIA (Stock Symbol NASDAQ: NVDA).",
            verbose=True,
        )

    def test_response_format(self):
        response = self.agent.invoke()
        messages = self.agent.workflow.channel.messages
        verified_response = self.llm_verification.verify(
            LLMVerification.get_verification_prompt()
            + "\n\n Task:" + self.agent.task
            + "\n\n Response:" + str(response)
            + "\n\n Collaboration Chat:\n" + "\n".join(messages)
        )

        self.assertIsInstance(
            response, RexiaAIResponse, "Response is not RexiaAIResponse."
        )
        
        self.assertTrue(verified_response, "Response verification failed")

if __name__ == "__main__":
    unittest.main()
