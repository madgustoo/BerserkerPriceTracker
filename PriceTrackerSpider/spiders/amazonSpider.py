import re
import scrapy
from volumes.models import Product, Retailer
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from PriceTrackerSpider.items import RetailerItem
from .util import strip_whitespace


# This Spider will crawl once a day
# Scrape amazon's canadian website to read and register PRICES and AVAILABILITY of Berserk mangas to the API
class AmazonSpider(scrapy.Spider):
    retailer_name = "amazon.ca"
    limit = 0
    name = "amazon"
    allowed_domains = ["amazon.ca"]

    start_urls = [
        "https://www.amazon.ca/s/ref=sr_pg_1?rh=n%3A916520%2Ck%3ABerserk+volume&keywords=Berserk+volume&ie=UTF8&qid=1484711680"
    ]

    def parse(self, response):

        # TODO: find a way to overwrite or to check if it retailer already exists and simply update instead of cleansing Retailer table
        # TODO: LOG CAUGHT ERRORS TO SEPARATE FILE LOOK INTO PYTHON LOGGING
        if self.limit == 0:
            Retailer.objects.filter(retailer_name__contains=self.retailer_name).delete()

        for section in response.xpath('//div[@class="s-item-container"]'):
            retailer_item = RetailerItem()
            title = section.xpath('.//h2/text()').extract_first()
            name = strip_whitespace(title)
            product_id = ''.join(x for x in title if x.isdigit())

            # Scrapes if Format: Berserk Volume 16
            if name.startswith("Berserk Volume") and name[-1:].isdigit() and len(name) < 20:
                retailer_item['retailer_name'] = self.retailer_name

                # Gets the product with its id (product_id) and adds or updates its amazon details
                try:
                    retailer_item['product'] = Product.objects.get(id=product_id)
                except (IntegrityError and ObjectDoesNotExist):
                    print("Volume #" + product_id + " does not exist in the database")
                else:
                    # If it does not raise an DoesNotExist exception
                    cost = section.xpath('.//span[contains(@class, "s-price")]/text()').extract_first()
                    if cost:
                        # Remove CAD$ from the price
                        price = re.sub('[CDN$]', '', cost)
                        retailer_item['price'] = float(price)
                    else:
                        # Some don't have a listed price from amazon nor have they an availability note
                        retailer_item['availability_note'] = "Unavailable"

                    # Also checks if the xpath didn't select a price value [$], because of amazon's dom format, this is hard to predict and so this workaround does great
                    availability = section.xpath(
                        './/div[contains(@class, "a-span7")]//div[3]//span/text()').extract_first()
                    if availability and "$" not in availability:

                        availability_test = strip_whitespace(availability.lower())
                        if availability_test == "eligible for free shipping" or availability_test == "get it by":
                            retailer_item['availability'] = True
                            retailer_item['availability_note'] = "In Stock"
                        elif availability_test.startswith("not in stock"):
                            retailer_item['availability'] = False
                            retailer_item['availability_note'] = "Not in Stock"
                        elif "pre-order" in availability_test:
                            retailer_item['availability'] = False
                            retailer_item['availability_note'] = availability
                        else:
                            retailer_item['availability'] = True
                            retailer_item['availability_note'] = availability

                    store_link = section.xpath('.//a/@href').extract_first()
                    if store_link:
                        retailer_item['store_link'] = store_link

                    # Saves to database / Expects duplicate keys, scraping is unpredictable at times
                    # Caught if this retailer already exists for this product
                    try:
                        retailer_item.save()
                    except IntegrityError:
                        print("Duplicate retailer " + self.retailer_name + " detected for Volume #" + product_id)

        # Crawl the next pages [limit = 3]
        next_page = response.xpath('//span[contains(@class, "pagnLink")]//a/@href').extract()
        if next_page and self.limit < 3:
            if self.limit == 0:
                next_page_url = next_page[0]
            else:
                next_page_url = next_page[1]
            self.limit += 1
            request = scrapy.Request(url="https://www.amazon.ca" + next_page_url)
            yield request
