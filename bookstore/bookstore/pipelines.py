# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from scrapy.exceptions import DropItem

class BookstorePipeline:

    def process_item(self, item):
        adapter = ItemAdapter(item)
        number_extract = lambda p: re.search(r"[\d.]+",p).group()
        keys_to_number = ["price","price_excl_tax","price_incl_tax","tax","availability"]
        numbers_lookup = {"One":1,"Two":2,"Three":3,"Four":4,"Five":5}
        # Treating numerical fields
        for key in adapter:
            if key in keys_to_number:
                adapter[key] = number_extract(adapter[key])
            if key in keys_to_number[:-2]: 
                adapter[key] = float(adapter[key])
        if float(adapter["price"]) < 0:
            raise DropItem("Invalid Price")
        availability = int(adapter["availability"])
        adapter["availability"] = availability
        adapter["in_stock"] = availability > 0
        rating = numbers_lookup.get(adapter["rating"].get().split('\n')[0].split('"')[-2].split(' ')[-1])
        if rating:
            adapter["rating"] = rating
        else:
            raise DropItem("Invalid or missing rating")
        upc = adapter.get("upc")
        if not upc:
            raise DropItem("Missing UPC")
        adapter["product_url"] = str(adapter["product_url"]).split()[-1].replace(">","")
        adapter["image_url"] = 'https://' + adapter["product_url"].split("/")[2] + '/' + str(adapter["image_url"]).replace("../../","")
        return item