# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

# <a>There is some text</a>

# Itemloader --> defines how the item is loaded. HA HA
# Takefirst --> extract the first value from the list of values
# MapCompose --> apply the list of functions to the list of values

def remove_commas(value):
    return value.replace(',', '')

def try_float(value):
    try:
        return float(value)
    except ValueError:
         return value
    
def try_int(value):
    try:
        return int(value)
    except ValueError:
        return value


class ShareMarketItem(scrapy.Item):
    # define the fields for your item here like:
    number = scrapy.Field( 
        input_processor = MapCompose(remove_tags, str.strip, remove_commas, try_int),
        output_processor = TakeFirst()
    )
    symbol = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    LTP = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, remove_commas, try_float),
        output_processor = TakeFirst()
    )
    percent_change = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, try_float),
        output_processor = TakeFirst()
    )
    high = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, remove_commas, try_float),
        output_processor = TakeFirst()
    )
    low = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, remove_commas, try_float),
        output_processor = TakeFirst()
    )
    open = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, remove_commas, try_float),
        output_processor = TakeFirst()
    )
    qty = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, remove_commas, try_int),
        output_processor = TakeFirst()
    )
    turnover = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, remove_commas, try_float),
        output_processor = TakeFirst()
    )
    symbol_href = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    

class HistoryStockItem(scrapy.Item):
    # define the fields for your item here like:
    number = scrapy.Field( 
        input_processor = MapCompose(remove_tags, str.strip, remove_commas, try_int),
        output_processor = TakeFirst()
    )
    date = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    LTP = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, remove_commas, try_float),
        output_processor = TakeFirst()
    )
    percent_change = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, try_float),
        output_processor = TakeFirst()
    )
    high = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, remove_commas, try_float),
        output_processor = TakeFirst()
    )
    low = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, remove_commas, try_float),
        output_processor = TakeFirst()
    )
    open = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, remove_commas, try_float),
        output_processor = TakeFirst()
    )
    qty = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, remove_commas, try_int),
        output_processor = TakeFirst()
    )
    turnover = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, remove_commas, try_float),
        output_processor = TakeFirst()
    )
   
    
