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
from share_market.items import HistoryStockItem
from selenium.webdriver.common.alert import Alert

class IndividualStocksSpider(scrapy.Spider):
    name = "individual_stocks"
    allowed_domains = ["merolagani.com"]
    company_name = "CHCL"
    start_urls = [f"https://merolagani.com/CompanyDetail.aspx?symbol={company_name}#0"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        

    def parse(self, response):
        self.driver.get(self.start_urls[0])

        # Handle potential alerts
        try:
            time.sleep(10)
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert = Alert(self.driver)
            alert.dismiss()  # or alert.accept() if you want to accept the alert
        except:
            pass  # No alert, proceed normally
       
        next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_lnkHistoryTab"]'))
                )
        time.sleep(2)
        next_button.click()
        time.sleep(2)
        self.driver.switch_to.alert.accept()
        time.sleep(2)


        while True:
            # Parse the page source with Scrapy's Selector
            response = Selector(text=self.driver.page_source)
            rows = response.css("tbody tr")[1:]
            time.sleep(3)
            for row in rows:
                item = ItemLoader(item=HistoryStockItem(), selector=row)
                item.add_css("number", 'td:nth-child(1)')
                item.add_css("date", 'td:nth-child(2)')
                item.add_css("LTP", 'td:nth-child(3)')
                item.add_css("percent_change", 'td:nth-child(4)')
                item.add_css("high", 'td:nth-child(5)')
                item.add_css("low", 'td:nth-child(6)')
                item.add_css("open", 'td:nth-child(7)')
                item.add_css("qty", 'td:nth-child(8)')
                item.add_css("turnover", 'td:nth-child(9)')
                
                print("Last Line")
                yield item.load_item()


            # Try to locate and click the "Next Page" button
            try:
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='pagging']//a[@title='Next Page']"))
                )
                time.sleep(3)
                next_button.click()
                time.sleep(3)
                
                
                
            except:  
                # Exit the loop if no "Next Page" button is found or clickable
                break

        self.driver.quit()

