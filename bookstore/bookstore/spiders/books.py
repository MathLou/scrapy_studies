import scrapy
import re
import json

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        # Extracting relative links
        links = [link for link in response.xpath('//div[@class="image_container"]/a/@href').getall()]
        # Appending to dict and returning
        for i in range(len(links)):
            # Scraping specific book page
            yield response.follow(links[i], callback=self.parse_book_page)
        # Pagination
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)

    def parse_book_page(self,response):
        """Parse each book page"""
        title = response.xpath('//div[@class="col-sm-6 product_main"]/h1/text()').get()
        price = response.xpath('//div[@class="col-sm-6 product_main"]/p[@class="price_color"]/text()').get()
        prod_info = response.xpath('//table[@class="table table-striped"]/tr/td/text()').getall()
        price_excl_tax = prod_info[2]
        price_incl_tax = prod_info[3]
        tax = prod_info[4]
        availability = prod_info[5]
        in_stock = ""
        rating = response.xpath('//p[has-class("star-rating")]')
        category = response.xpath('//ul[@class="breadcrumb"]/li/a/text()').getall()[-1]
        upc = prod_info[0]
        product_type = prod_info[1]
        num_reviews = int(prod_info[6])
        description = response.xpath('//article[@class="product_page"]/p/text()').get()
        image_url = response.xpath('//div[@class="item active"]/img/@src').get()
        product_url = response
        yield {
            "title":title,
            "price":price,
            "price_excl_tax":price_excl_tax,
            "price_incl_tax":price_incl_tax,
            "tax":tax,
            "availability":availability,
            "in_stock":in_stock,
            "rating": rating,
            "category":category,
            "upc" : upc,
            "product_type" : product_type,
            "num_reviews" : num_reviews,
            "description" : description,
            "image_url" : image_url,
            "product_url" : product_url
        }