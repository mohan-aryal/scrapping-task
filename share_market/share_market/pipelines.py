# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3

from datetime import datetime
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


# to see whether the data we are scrapping is of good format or not if not exlclude those items.
class IndividualShareMarketPipeline:

    def process_item(self, item, spider):
        # Check if "date" exists in the item
        if "date" not in item:
            raise DropItem(f"Missing date in item: {item}")

        # Validate the date format
        try:
            datetime.strptime(item["date"], "%Y/%m/%d")
        except ValueError:
            raise DropItem(f"Invalid date format in item: {item['date']}")

        # if "qty" not in item or not isinstance(item.get("qty"), int):
        #     item["qty"] = 0  # Assign a default value or handle the missing key appropriately
        # # Continue processing the item
        return item
    
            



class ShareMarketPipeline:
    def process_item(self, item, spider):
        if not isinstance(item["qty"], int):
            raise DropItem("Missing qty value. Item excluded")
        return item
    
# OK let's save this shit to the database. AH! AH!
# Let's use simple sqlite3 here, which is simple to user for now.

class SaveToDatabasePipeline:
    def __init__(self):
        self.con = sqlite3.connect("share_data.db") # if this doesn't exist then it will create one.
        self.cur = self.con.cursor()
    
    def open_spider(self, spider):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS share_data (
                share_id INTEGER PRIMARY KEY,
                symbol TEXT,
                LTP REAL,
                percent_change INTEGER,
                high REAL,
                low REAL,
                open REAL,
                qty INTEGER,
                turnover REAL,
                symbol_href TEXT
            )
        """)
        self.con.commit()


    def process_item(self, item, spider):
        if item is None:
            spider.logger.error("Received NoneType item. Skipping...")
            return
        try:
            self.con.execute("""
                INSERT INTO share_data (symbol, LTP, percent_change, high, low, open, qty, turnover, symbol_href)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (item["symbol"], item["LTP"], item["percent_change"], item["high"],
                item["low"], item["open"], item["qty"], item["turnover"], item["symbol_href"]))
            self.con.commit()

            return item
           
        
        except Exception as e:
            spider.logger.error(f"Failed to insert item into database: {e}")
        
    def close_spider(self, spider):
        self.con.close()

        
# class NoDuplicateShareData:
#     def __init__(self):
#         self.symbol_seen = set()
    
#     def process_item(self, item, spider):
#         if item["symbol"].lower() in self.symbol_seen:
#             raise DropItem(f"Duplicate symbol found: {item}")
#         else:
#             self.symbol_seen.add(item["symbol"].lower())
#             return item

        
