import scrapy
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from share_market.items import ShareMarketItem
from webdriver_manager.chrome import ChromeDriverManager
import time

class StocksSpider(scrapy.Spider):
    name = "stocks"
    allowed_domains = ["merolagani.com"]
    start_urls = ["https://merolagani.com/StockQuote.aspx"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        

    def parse(self, response):
        self.driver.get(self.start_urls[0])

        while True:
            # Parse the page source with Scrapy's Selector
            response = Selector(text=self.driver.page_source)
            rows = response.css("tbody tr")
            for row in rows:
                item = ItemLoader(item=ShareMarketItem(), selector=row)
                item.add_css("number", 'td:nth-child(1)')
                item.add_css("symbol", 'td:nth-child(2) a')
                item.add_css("LTP", 'td:nth-child(3)')
                item.add_css("percent_change", 'td:nth-child(4)')
                item.add_css("high", 'td:nth-child(5)')
                item.add_css("low", 'td:nth-child(6)')
                item.add_css("open", 'td:nth-child(7)')
                item.add_css("qty", 'td:nth-child(8)')
                item.add_css("turnover", 'td:nth-child(9)')
                item.add_css("symbol_href", 'td.text-center a::attr(href)')

                yield item.load_item()

            # Try to locate and click the "Next Page" button
            try:
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='pagging']//a[@title='Next Page']"))
                )
                time.sleep(10)
                next_button.click()
                time.sleep(5)
                self.driver.switch_to.alert.accept()
                time.sleep(3)
                
            except:  
                # Exit the loop if no "Next Page" button is found or clickable
                break

        self.driver.quit()

