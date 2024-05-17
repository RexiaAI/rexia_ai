# selemium_handler.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class SeleniumHandler:
    """Handler for Selenium WebDriver for Chrome."""

    def __init__(self):
        """Initialize the Selenium WebDriver with options."""
        self.options = Options()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def get(self, url: str):
        """
        Navigate the WebDriver to the specified URL.

        Parameters:
        url (str): The URL to navigate to.

        Returns:
        result: The result of the navigation.
        """
        result = self.driver.get(url)
        return result

    def close(self):
        """Close the WebDriver."""
        self.driver.quit()