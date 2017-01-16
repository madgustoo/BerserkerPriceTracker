import re
import scrapy
from django.core.exceptions import ObjectDoesNotExist
from PriceTrackerSpider.items import RetailerItem
from volumes.models import Product, Retailer


# This Spider will crawl once a day
# Scrape amazon's canadian website to read and register PRICES and AVAILABILITY of berserk mangas to the API
class AmazonSpider(scrapy.Spider):
    retailer_name = "amazon.ca"
    retailer_id = 1
    limit = 0
    name = "amazon"
    allowed_domains = ["amazon.ca"]

    start_urls = [
        "https://www.amazon.ca/s/ref=sr_pg_3?rh=n%3A916520%2Ck%3ABerserk+volume&page=3&keywords=Berserk+volume&ie=UTF8&qid=1484536936"
    ]

    def parse(self, response):

        if self.limit == 0:
            Retailer.objects.filter(retailer_name__contains=self.retailer_name).delete()

        for section in response.xpath('//div[@class="s-item-container"]'):
            retailer_item = RetailerItem()
            title = section.xpath('.//h2/text()').extract_first()
            name = ' '.join(title.split())
            product_id = ''.join(x for x in name if x.isdigit())

            # TODO: find a way to overwrite or to check if it retailer already exists and simply update

            # Scrapes if Format: Berserk Volume 16
            if name.startswith("Berserk Volume") and name[-1:].isdigit():
                # retailer_item['id'] = self.retailer_id
                retailer_item['retailer_name'] = self.retailer_name

                # Gets the product with its id (product_id) and adds or updates its amazon details
                try:
                    retailer_item['product'] = Product.objects.get(id=product_id)
                except ObjectDoesNotExist:
                    print("Volume #" + product_id + " does not exist")
                    pass
                else:
                    # If it does not raise an DoesNotExist exception
                    cost = section.xpath('.//span[contains(@class, "s-price")]/text()').extract_first()
                    if cost:
                        # Remove CAD$ from the price
                        price = re.sub('[CDN$]', '', cost)
                        retailer_item['price'] = float(price)
                    else:
                        retailer_item['price'] = None

                    store_link = section.xpath('.//a/@href').extract_first()
                    if store_link:
                        retailer_item['store_link'] = store_link
                    else:
                        retailer_item['store_link'] = 0

                    availability = section.xpath(
                        './/div[contains(@class, "a-span7")]//div[4]//span/text()').extract_first()
                    # Also checks if the xpath didn't select a price value [$], because of amazon's dom format, this is hard to predict and so this workaround does great
                    if availability and "$" not in availability:
                        retailer_item['availability'] = availability
                    else:
                        retailer_item['availability'] = "Not sold by Amazon.ca"

                # Save to database
                retailer_item.save()

        # Crawl the next pages [limit = 4]
        next_page = response.xpath('//span[contains(@class, "pagnLink")]//a/@href').extract()
        if next_page and self.limit < 4:
            if self.limit == 0:
                next_page_url = next_page[0]
            else:
                next_page_url = next_page[1]
            self.limit += 1
            request = scrapy.Request(url="https://www.amazon.ca" + next_page_url)
            yield request
