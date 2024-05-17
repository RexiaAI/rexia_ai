# selemium_handler.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class selenium_handler:
    def __init__(self):
        self.options = Options()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def get(self, url):
        result = self.driver.get(url)
        return result

    def close(self):
        self.driver.quit()