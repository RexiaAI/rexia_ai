""" ReXia.AI Alpha Vantage Tool - AlphaVantageAPIWrapper extended to work with ReXia.AI. 
Credit to the original authors who did most of the work. Should not be used without an LLM that
can handle very large datasets being returned."""

import logging
from typing import Dict, List
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper
from ..base import BaseTool

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class RexiaAIAlphaVantageSearchSymbols(BaseTool):
    """
    Symbol searching tool for ReXia.AI.

    Attributes
    ----------
    api_key : str
        The API key for AlphaVantage.

    Methods
    -------
    search_symbols(keywords: str) -> str:
        Make a request to the AlphaVantage API to search for symbols.
    to_rexiaai_tool() -> list:
        Return the tool as a JSON object for ReXia.AI.
    to_rexiaai_function_call() -> dict:
        Return the tool as a dictionary object for ReXia.AI.
    """

    def __init__(self, api_key: str):
        """
        Constructs all the necessary attributes for the RexiaAIAlphaVantageSearchSymbols object.

        Parameters
        ----------
            api_key : str
                The API key for AlphaVantage.
        """
        super().__init__(
            name="search_symbols",
            func=self.search_symbols,
            description="Make a request to the AlphaVantage API to search for symbols.",
        )
        self.api_key = api_key
        self.alpha_vantage_api = AlphaVantageAPIWrapper(alphavantage_api_key=api_key)

    def search_symbols(self, keywords: str) -> str:
        """
        Make a request to the AlphaVantage API to search for symbols.

        Parameters
        ----------
            keywords : str
                The symbols you wish to search for results on.

        Returns
        -------
            str
                The search result.
        """
        try:
            result = self.alpha_vantage_api.search_symbols(keywords)
        except Exception as e:
            logger.error(f"An error occurred while searching symbols: {e}")
            return None
        return result

    def to_rexiaai_tool(self) -> list:
        """
        Return the tool as a JSON object for ReXia.AI.

        Returns
        -------
            list
                The tool as a JSON object.
        """
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

    def to_rexiaai_function_call(self) -> dict:
        """
        Return the tool as a dictionary object for ReXia.AI.

        Returns
        -------
            dict
                The tool as a dictionary object.
        """
        function_call = {"name": "search_symbols"}

        return function_call


class RexiaAIAlphaVantageMarketNewsSentiment(BaseTool):
    """
    Market news sentiment tool for ReXia.AI.

    Attributes:
        api_key (str): The API key for AlphaVantage.
        alpha_vantage_api (AlphaVantageAPIWrapper): The AlphaVantage API wrapper instance.
    """

    def __init__(self, api_key: str):
        """
        Initialize the RexiaAIAlphaVantageMarketNewsSentiment instance.

        Args:
            api_key (str): The API key for AlphaVantage.
        """
        super().__init__(
            name="get_market_news_sentiment",
            func=self.get_market_news_sentiment,
            description="Make a request to the AlphaVantage API to get market news sentiment for a given symbol.",
        )
        self.api_key = api_key
        self.alpha_vantage_api = AlphaVantageAPIWrapper(alphavantage_api_key=api_key)

    def get_market_news_sentiment(self, symbol: str) -> str:
        """
        Make a request to the AlphaVantage API to get market news sentiment for a given symbol.

        Args:
            symbol (str): The symbol you wish to search for results on.

        Returns:
            str: The market news sentiment data.
        """
        try:
            result = self.alpha_vantage_api._get_market_news_sentiment(symbol)
        except Exception as e:
            logger.error(f"An error occurred while searching symbols: {e}")
            return None
        return result

    def to_rexiaai_tool(self) -> List[Dict]:
        """
        Return the tool as a JSON object for ReXia.AI.

        Returns:
            List[Dict]: The tool as a JSON object.
        """
        tool = [
            {
                "name": "get_market_news_sentiment",
                "description": "Make a request to the AlphaVantage API to get market news sentiment for a given symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The symbol you wish to search for results on. Should contain only the stock symbols. e.g. 'AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT', 'NVDA'",
                        }
                    },
                    "required": ["symbol"],
                },
            }
        ]
        return tool

    def to_rexiaai_function_call(self) -> Dict:
        """
        Return the tool as a dictionary object for ReXia.AI.

        Returns:
            Dict: The tool as a dictionary object.
        """
        function_call = {"name": "get_market_news_sentiment"}
        return function_call


class RexiaAIAlphaVantageTimeSeriesDaily(BaseTool):
    """
    Time series daily tool for ReXia.AI.

    Attributes:
        api_key (str): The API key for AlphaVantage.
        alpha_vantage_api (AlphaVantageAPIWrapper): The AlphaVantage API wrapper instance.
    """

    def __init__(self, api_key: str):
        """
        Initialize the RexiaAIAlphaVantageTimeSeriesDaily instance.

        Args:
            api_key (str): The API key for AlphaVantage.
        """
        super().__init__(
            name="get_time_series_daily",
            func=self.get_time_series_daily,
            description="Make a request to the AlphaVantage API to get time series daily data for a given symbol.",
        )
        self.api_key = api_key
        self.alpha_vantage_api = AlphaVantageAPIWrapper(alphavantage_api_key=api_key)

    def get_time_series_daily(self, symbol: str) -> str:
        """
        Make a request to the AlphaVantage API to get time series daily data for a given symbol.

        Args:
            symbol (str): The symbol you wish to search for results on.

        Returns:
            str: The time series daily data.
        """
        try:
            result = self.alpha_vantage_api._get_time_series_daily(symbol)
        except Exception as e:
            logger.error(f"An error occurred while searching symbols: {e}")
            return None
        return result

    def to_rexiaai_tool(self) -> List[Dict]:
        """
        Return the tool as a JSON object for ReXia.AI.

        Returns:
            List[Dict]: The tool as a JSON object.
        """
        tool = [
            {
                "name": "get_time_series_daily",
                "description": "Make a request to the AlphaVantage API to get time series daily data for a given symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The symbol you wish to search for results on. Should contain only the stock symbols. e.g. 'AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT', 'NVDA'",
                        }
                    },
                    "required": ["symbol"],
                },
            }
        ]
        return tool

    def to_rexiaai_function_call(self) -> Dict:
        """
        Return the tool as a dictionary object for ReXia.AI.

        Returns:
            Dict: The tool as a dictionary object.
        """
        function_call = {"name": "get_time_series_daily"}
        return function_call


class RexiaAIAlphaVantageQuoteEndpoint(BaseTool):
    """
    Quote endpoint tool for ReXia.AI.

    Attributes:
        api_key (str): The API key for AlphaVantage.
        alpha_vantage_api (AlphaVantageAPIWrapper): The AlphaVantage API wrapper instance.
    """

    def __init__(self, api_key: str):
        """
        Initialize the RexiaAIAlphaVantageQuoteEndpoint instance.

        Args:
            api_key (str): The API key for AlphaVantage.
        """
        super().__init__(
            name="get_quote_endpoint",
            func=self.get_quote_endpoint,
            description="Make a request to the AlphaVantage API to get quote data for a given symbol.",
        )
        self.api_key = api_key
        self.alpha_vantage_api = AlphaVantageAPIWrapper(alphavantage_api_key=api_key)

    def get_quote_endpoint(self, symbol: str) -> str:
        """
        Make a request to the AlphaVantage API to get quote data for a given symbol.

        Args:
            symbol (str): The symbol you wish to search for results on.

        Returns:
            str: The quote data.
        """
        try:
            result = self.alpha_vantage_api._get_quote_endpoint(symbol)
        except Exception as e:
            logger.error(f"An error occurred while searching symbols: {e}")
            return None
        return result

    def to_rexiaai_tool(self) -> List[Dict]:
        """
        Return the tool as a JSON object for ReXia.AI.

        Returns:
            List[Dict]: The tool as a JSON object.
        """
        tool = [
            {
                "name": "get_quote_endpoint",
                "description": "Make a request to the AlphaVantage API to get quote data for a given symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The symbol you wish to search for results on. Should contain only the stock symbols. e.g. 'AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT', 'NVDA'",
                        }
                    },
                    "required": ["symbol"],
                },
            }
        ]
        return tool

    def to_rexiaai_function_call(self) -> Dict:
        """
        Return the tool as a dictionary object for ReXia.AI.

        Returns:
            Dict: The tool as a dictionary object.
        """
        function_call = {"name": "get_quote_endpoint"}
        return function_call


class RexiaAIAlphaVantageTimeSeriesWeekly(BaseTool):
    """
    Time series weekly tool for ReXia.AI.

    Attributes:
        api_key (str): The API key for AlphaVantage.
        alpha_vantage_api (AlphaVantageAPIWrapper): The AlphaVantage API wrapper instance.
    """

    def __init__(self, api_key: str):
        """
        Initialize the RexiaAIAlphaVantageTimeSeriesWeekly instance.

        Args:
            api_key (str): The API key for AlphaVantage.
        """
        super().__init__(
            name="get_time_series_weekly",
            func=self.get_time_series_weekly,
            description="Make a request to the AlphaVantage API to get time series weekly data for a given symbol.",
        )
        self.api_key = api_key
        self.alpha_vantage_api = AlphaVantageAPIWrapper(alphavantage_api_key=api_key)

    def get_time_series_weekly(self, symbol: str) -> str:
        """
        Make a request to the AlphaVantage API to get time series weekly data for a given symbol.

        Args:
            symbol (str): The symbol you wish to search for results on.

        Returns:
            str: The time series weekly data.
        """
        try:
            result = self.alpha_vantage_api._get_time_series_weekly(symbol)
        except Exception as e:
            logger.error(f"An error occurred while searching symbols: {e}")
            return None
        return result

    def to_rexiaai_tool(self) -> List[Dict]:
        """
        Return the tool as a JSON object for ReXia.AI.

        Returns:
            List[Dict]: The tool as a JSON object.
        """
        tool = [
            {
                "name": "get_time_series_weekly",
                "description": "Make a request to the AlphaVantage API to get time series weekly data for a given symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The symbol you wish to search for results on. Should contain only the stock symbols. e.g. 'AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT', 'NVDA'",
                        }
                    },
                    "required": ["symbol"],
                },
            }
        ]
        return tool

    def to_rexiaai_function_call(self) -> Dict:
        """
        Return the tool as a dictionary object for ReXia.AI.

        Returns:
            Dict: The tool as a dictionary object.
        """
        function_call = {"name": "get_time_series_weekly"}
        return function_call


class RexiaAIAlphaVantageTopGainersLosers(BaseTool):
    """
    Top gainers and losers tool for ReXia.AI.

    Attributes:
        api_key (str): The API key for AlphaVantage.
        alpha_vantage_api (AlphaVantageAPIWrapper): The AlphaVantage API wrapper instance.
    """

    def __init__(self, api_key: str):
        """
        Initialize the RexiaAIAlphaVantageTopGainersLosers instance.

        Args:
            api_key (str): The API key for AlphaVantage.
        """
        super().__init__(
            name="get_top_gainers_losers",
            func=self.get_top_gainers_losers,
            description="Make a request to the AlphaVantage API to get top gainers and losers.",
        )
        self.api_key = api_key
        self.alpha_vantage_api = AlphaVantageAPIWrapper(alphavantage_api_key=api_key)

    def get_top_gainers_losers(self) -> str:
        """
        Make a request to the AlphaVantage API to get top gainers and losers.

        Returns:
            str: The top gainers and losers data.
        """
        try:
            result = self.alpha_vantage_api._get_top_gainers_losers()
        except Exception as e:
            logger.error(f"An error occurred while searching symbols: {e}")
            return None
        return result

    def to_rexiaai_tool(self) -> List[Dict]:
        """
        Return the tool as a JSON object for ReXia.AI.

        Returns:
            List[Dict]: The tool as a JSON object.
        """
        tool = [
            {
                "name": "get_top_gainers_losers",
                "description": "Make a request to the AlphaVantage API to get top gainers and losers.",
            }
        ]
        return tool

    def to_rexiaai_function_call(self) -> Dict:
        """
        Return the tool as a dictionary object for ReXia.AI.

        Returns:
            Dict: The tool as a dictionary object.
        """
        function_call = {"name": "get_top_gainers_losers"}
        return function_call


class RexiaAIAlphaVantageExchangeRate(BaseTool):
    """
    Exchange rate tool for ReXia.AI.

    Attributes:
        api_key (str): The API key for AlphaVantage.
        alpha_vantage_api (AlphaVantageAPIWrapper): The AlphaVantage API wrapper instance.
    """

    def __init__(self, api_key: str):
        """
        Initialize the RexiaAIAlphaVantageExchangeRate instance.

        Args:
            api_key (str): The API key for AlphaVantage.
        """
        super().__init__(
            name="get_exchange_rate",
            func=self.get_exchange_rate,
            description="Make a request to the AlphaVantage API to get exchange rate data.",
        )
        self.api_key = api_key
        self.alpha_vantage_api = AlphaVantageAPIWrapper(alphavantage_api_key=api_key)

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> str:
        """
        Make a request to the AlphaVantage API to get exchange rate data.

        Args:
            from_currency (str): The currency you wish to convert from.
            to_currency (str): The currency you wish to convert to.

        Returns:
            str: The exchange rate data.
        """
        try:
            result = self.alpha_vantage_api._get_exchange_rate(
                from_currency, to_currency
            )
        except Exception as e:
            logger.error(f"An error occurred while searching symbols: {e}")
            return None
        return result

    def to_rexiaai_tool(self) -> List[Dict]:
        """
        Return the tool as a JSON object for ReXia.AI.

        Returns:
            List[Dict]: The tool as a JSON object.
        """
        tool = [
            {
                "name": "get_exchange_rate",
                "description": "Make a request to the AlphaVantage API to get exchange rate data.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "from_currency": {
                            "type": "string",
                            "description": "The currency you wish to convert from. e.g. 'USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD'",
                        },
                        "to_currency": {
                            "type": "string",
                            "description": "The currency you wish to convert to. e.g. 'USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD'",
                        },
                    },
                    "required": ["from_currency", "to_currency"],
                },
            }
        ]
        return tool

    def to_rexiaai_function_call(self) -> Dict:
        """
        Return the tool as a dictionary object for ReXia.AI.

        Returns:
            Dict: The tool as a dictionary object.
        """
        function_call = {"name": "get_exchange_rate"}
        return function_call
