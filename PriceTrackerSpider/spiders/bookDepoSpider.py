import re
import scrapy
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from PriceTrackerSpider.items import RetailerItem
from volumes.models import Product, Retailer
from .util import strip_whitespace


# This Spider will crawl once a day
# Scrape amazon's canadian website to read and register PRICES and AVAILABILITY of berserk mangas to the API
class BookDepoSpider(scrapy.Spider):
    domain = "https://www.bookdepository.com"
    retailer_name = "bookdepository.com"
    limit = 0
    name = "bookdepo"
    allowed_domains = ["bookdepository.com"]

    start_urls = [
        "https://www.bookdepository.com/search?searchTerm=berserk&search=Find+book"
    ]

    def parse(self, response):
        if self.limit == 0:
            Retailer.objects.filter(retailer_name__contains=self.retailer_name).delete()

        for section in response.xpath('//div[@class="book-item"]'):
            retailer_item = RetailerItem()
            title = section.xpath('.//h3[@class="title"]/a/text()').extract_first()
            name = strip_whitespace(title)
            product_id = ''.join(x for x in title if x.isdigit())

            # Scrapes if Format: Starts with Berserk: and ends with a number
            if name.startswith("Berserk:") and name[-1:].isdigit():
                retailer_item['retailer_name'] = self.retailer_name

                # Gets the product with its id (product_id) and adds or updates its bookdepo details
                try:
                    retailer_item['product'] = Product.objects.get(id=product_id)
                except (IntegrityError and ObjectDoesNotExist):
                    print("Volume #" + product_id + " does not exist in the database")
                    pass
                else:
                    cost = section.xpath('.//p[@class="price"]/text()').extract_first()
                    if cost:
                        # Remove C$ from the price
                        price = re.sub('[C$]', '', cost)
                        retailer_item['price'] = float(price)
                        retailer_item['availability'] = True
                        retailer_item['availability_note'] = "In Stock"
                    else:
                        retailer_item['availability'] = False
                        retailer_item['availability_note'] = "Not in Stock"

                    store_link = section.xpath('.//h3[@class="title"]//a/@href').extract_first()
                    if store_link:
                        retailer_item['store_link'] = self.domain + store_link

                # Save to database
                retailer_item.save()

        # Crawl the next pages [limit = 3]
        next_page = response.xpath('//ul[contains(@class, "responsive-pagination")]/li/a/@href').extract()
        if next_page and self.limit < 3:
            self.limit += 1
            next_page_url = next_page[self.limit]
            request = scrapy.Request(url=self.domain + next_page_url)
            yield request
