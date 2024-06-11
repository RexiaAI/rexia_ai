""" Rexia AI Alpha Vantage Tool - Alpha Vantage Tool from langchain_community extended to work more 
consistently with open source models within ReXia.AI. Credit to the original authors who did most of
the work. This implementation is a bit clunky, but seems to be the best way to keep the llm from getting
confused. Hopefully, this will be refactored in the future."""

from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper
from ..base import BaseTool


class RexiaAIAlphaVantageSearchSymbols(BaseTool):
    """Symbol searching tool for ReXia.AI."""

    api_key: str

    def __init__(self, api_key: str):
        super().__init__(
            name="search_symbols",
            func=self.search_symbols,
            description="Make a request to the AlphaVantage API to search for symbols.",
        )
        self.api_key = api_key
        self.alpha_vantage_api = AlphaVantageAPIWrapper(alphavantage_api_key=api_key)

    def search_symbols(self, keywords: str) -> str:
        """Make a request to the AlphaVantage API to search for symbols."""
        return self.alpha_vantage_api.search_symbols(keywords)
    
    def to_rexiaai_tool(self):
        """Return the tool as a JSON object for ReXia.AI."""

        tool = [
            {
                "name": "search_symbols",
                "description": "Make a request to the AlphaVantage API to search for symbols.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "type": "string",
                            "description": "The symbols you wish to search for results on. Should contain only the stock symbols."
                            "e.g. 'AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT', 'NVDA'",
                        },
                    },
                    "required": ["keywords"],
                },
            },
        ]

        return tool
    
    def to_rexiaai_function_call(self):
        """Return the tool as a dictionary object for ReXia.AI."""
        function_call = {"name": "search_symbols"}

        return function_call



class RexiaAIAlphaVantageMarketNewsSentiment(BaseTool):
    """Market news sentiment tool for ReXia.AI."""

    api_key: str

    def __init__(self, api_key: str):
        super().__init__(
            name="get_market_news_sentiment",
            func=self.get_market_news_sentiment,
            description="Make a request to the AlphaVantage API to get market news sentiment for a given symbol.",
        )
        self.api_key = api_key
        self.alpha_vantage_api = AlphaVantageAPIWrapper(alphavantage_api_key=api_key)

    def get_market_news_sentiment(self, symbol: str) -> str:
        """Make a request to the AlphaVantage API to get market news sentiment for a given symbol."""
        return self.alpha_vantage_api._get_market_news_sentiment(symbol)
    
    def to_rexiaai_tool(self):
        """Return the tool as a JSON object for ReXia.AI."""

        tool = [
            {
                "name": "get_market_news_sentiment",
                "description": "Make a request to the AlphaVantage API to get market news sentiment for a given symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The symbol you wish to search for results on. Should contain only the stock symbols."
                            "e.g. 'AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT', 'NVDA'",
                        },
                    },
                    "required": ["symbol"],
                },
            },
        ]
            
        return tool
        
    def to_rexiaai_function_call(self):
        """Return the tool as a dictionary object for ReXia.AI."""
        function_call = {"name": "get_market_news_sentiment"}
        
        return function_call


class RexiaAIAlphaVantageTimeSeriesDaily(BaseTool):
    """Time series daily tool for ReXia.AI."""

    api_key: str

    def __init__(self, api_key: str):
        super().__init__(
            name="get_time_series_daily",
            func=self.get_time_series_daily,
            description="Make a request to the AlphaVantage API to get time series daily data for a given symbol.",
        )
        self.api_key = api_key
        self.alpha_vantage_api = AlphaVantageAPIWrapper(alphavantage_api_key=api_key)

    def get_time_series_daily(self, symbol: str) -> str:
        """Make a request to the AlphaVantage API to get time series daily data for a given symbol."""
        return self.alpha_vantage_api._get_time_series_daily(symbol)
    
    def to_rexiaai_tool(self):
        """Return the tool as a JSON object for ReXia.AI."""

        tool = [
            {
                "name": "get_time_series_daily",
                "description": "Make a request to the AlphaVantage API to get time series daily data for a given symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The symbol you wish to search for results on. Should contain only the stock symbols."
                            "e.g. 'AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT', 'NVDA'",
                        },
                    },
                    "required": ["symbol"],
                },
            },
        ]
            
        return tool
        
    
    def to_rexiaai_function_call(self):
        """Return the tool as a dictionary object for ReXia.AI."""
        function_call = {"name": "get_time_series_daily"}
        
        return function_call


class RexiaAIAlphaVantageQuoteEndpoint(BaseTool):
    """Quote endpoint tool for ReXia.AI."""

    api_key: str

    def __init__(self, api_key: str):
        super().__init__(
            name="get_quote_endpoint",
            func=self.get_quote_endpoint,
            description="Make a request to the AlphaVantage API to get quote data for a given symbol.",
        )
        self.api_key = api_key
        self.alpha_vantage_api = AlphaVantageAPIWrapper(alphavantage_api_key=api_key)

    def get_quote_endpoint(self, symbol: str) -> str:
        """Make a request to the AlphaVantage API to get quote data for a given symbol."""
        return self.alpha_vantage_api._get_quote_endpoint(symbol)
    
    def to_rexiaai_tool(self):
        """Return the tool as a JSON object for ReXia.AI."""

        tool = [
            {
                "name": "get_quote_endpoint",
                "description": "Make a request to the AlphaVantage API to get quote data for a given symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The symbol you wish to search for results on. Should contain only the stock symbols."
                            "e.g. 'AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT', 'NVDA'",
                        },
                    },
                    "required": ["symbol"],
                },
            },
        ]
            
        return tool
        
    
    def to_rexiaai_function_call(self):
        """Return the tool as a dictionary object for ReXia.AI."""
        function_call = {"name": "get_quote_endpoint"}
        
        return function_call


class RexiaAIAlphaVantageTimeSeriesWeekly(BaseTool):
    """Time series weekly tool for ReXia.AI."""

    api_key: str

    def __init__(self, api_key: str):
        super().__init__(
            name="get_time_series_weekly",
            func=self.get_time_series_weekly,
            description="Make a request to the AlphaVantage API to get time series weekly data for a given symbol.",
        )
        self.api_key = api_key
        self.alpha_vantage_api = AlphaVantageAPIWrapper(alphavantage_api_key=api_key)

    def get_time_series_weekly(self, symbol: str) -> str:
        """Make a request to the AlphaVantage API to get time series weekly data for a given symbol."""
        return self.alpha_vantage_api._get_time_series_weekly(symbol)
    
    def to_rexiaai_tool(self):
        """Return the tool as a JSON object for ReXia.AI."""

        tool = [
            {
                "name": "get_time_series_weekly",
                "description": "Make a request to the AlphaVantage API to get time series weekly data for a given symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The symbol you wish to search for results on. Should contain only the stock symbols."
                            "e.g. 'AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT', 'NVDA'",
                        },
                    },
                    "required": ["symbol"],
                },
            },
        ]
            
        return tool
        
        
    def to_rexiaai_function_call(self):
        """Return the tool as a dictionary object for ReXia.AI."""
        function_call = {"name": "get_time_series_weekly"}
        
        return function_call


class RexiaAIAlphaVantageTopGainersLosers(BaseTool):
    """Top gainers and losers tool for ReXia.AI."""

    api_key: str

    def __init__(self, api_key: str):
        super().__init__(
            name="get_top_gainers_losers",
            func=self.get_top_gainers_losers,
            description="Make a request to the AlphaVantage API to get top gainers and losers..",
        )
        self.api_key = api_key
        self.alpha_vantage_api = AlphaVantageAPIWrapper(alphavantage_api_key=api_key)

    def get_top_gainers_losers(self) -> str:
        """Make a request to the AlphaVantage API to get top gainers and losers."""
        return self.alpha_vantage_api._get_top_gainers_losers()
    
    def to_rexiaai_tool(self):
        """Return the tool as a JSON object for ReXia.AI."""

        tool = [
            {
                "name": "get_top_gainers_losers",
                "description": "Make a request to the AlphaVantage API to get top gainers and losers.",
            },
        ]
            
        return tool
        
        
    def to_rexiaai_function_call(self):
        """Return the tool as a dictionary object for ReXia.AI."""
        function_call = {"name": "get_top_gainers_losers"}
        
        return function_call


class RexiaAIAlphaVantageExchangeRate(BaseTool):
    """Exchange rate tool for ReXia.AI."""

    api_key: str
    
    def __init__(self, api_key: str):
        super().__init__(
            name="get_exchange_rate",
            func=self.get_exchange_rate,
            description="Make a request to the AlphaVantage API to get exchange rate data.",
        )
        self.api_key = api_key
        self.alpha_vantage_api = AlphaVantageAPIWrapper(alphavantage_api_key=api_key)

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> str:
        """Make a request to the AlphaVantage API to get exchange rate data."""
        return self.alpha_vantage_api._get_exchange_rate(from_currency, to_currency)
    
    def to_rexiaai_tool(self):
        """Return the tool as a JSON object for ReXia.AI."""

        tool = [
            {
                "name": "get_exchange_rate",
                "description": "Make a request to the AlphaVantage API to get exchange rate data..",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "from_currency": {
                            "type": "string",
                            "description": "The currency you wish to convert from."
                            "e.g. 'USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD'",
                        },
                        "to_currency": {
                            "type": "string",
                            "description": "The currency you wish to convert to."
                            "e.g. 'USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD'",
                        },
                    },
                    "required": ["from_currency", "to_currency"],
                },
            },
        ]
            
        return tool
        
        
    def to_rexiaai_function_call(self):
        """Return the tool as a dictionary object for ReXia.AI."""
        function_call = {"name": "get_exchange_rate"}
        
        return function_call

