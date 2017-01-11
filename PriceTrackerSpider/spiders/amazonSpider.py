import re
import scrapy
import datetime
from PriceTrackerSpider.items import AmazonItem


# Scrape amazon's canadian website to read and register the latest prices of berserk mangas to the API
class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.ca"]

    start_urls = [
        # Shorten this link
        "https://www.amazon.ca/s/ref=nb_sb_ss_i_1_7?url=search-alias%3Dstripbooks&field-keywords=berserk&sprefix=berserk%2Caps%2C140&crid=2EQUOUQ7COBVX"
    ]

    def parse(self, response):
        # Section is a amazon search result, which is a div with the HTML class s-tem-container
        for section in response.xpath('//div[@class="s-item-container"]'):
            item = AmazonItem()

            title = section.xpath('.//h2/text()').extract_first()
            # Substitute multiple whitespace with a single whitespace
            name = ' '.join(title.split())

            # Checks to see if it's truly the product that we want to scrape
            # Scrapes if Format: Berserk Volume 16
            if name.startswith("Berserk") and name[-1:].isdigit():
                # Name of the product
                item['name'] = name
                # ID is the volume's number / Gets extracted from the title then converted to an int
                item['id'] = int(''.join(x for x in title if x.isdigit()))
                # Date of first english release in NA
                date = section.xpath('.//span[3][contains(@class, "a-color-secondary")]/text()').extract_first()
                if len(date) > 4:
                    publication_date = datetime.datetime.strptime(date, '%b %d %Y').date()
                    item['publication_date'] = publication_date
                else:
                    item['publication_date'] = None
                # Remove CAD$ from the price
                cost = section.xpath('.//span[contains(@class, "s-price")]/text()').extract_first()
                price = re.sub('[ CDN$]', '', cost)
                item['price'] = float(price)
                # Image
                item['image'] = section.xpath('.//img/@src').extract_first()
                # Link to the item in amazon
                item['store_link'] = section.xpath('.//a/@href').extract_first()
                yield item
