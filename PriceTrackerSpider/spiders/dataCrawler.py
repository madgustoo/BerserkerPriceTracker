import re
import scrapy
import datetime
from PriceTrackerSpider.items import AmazonItem, RetailerItem


# This Spider will run once a month, at the end of each to gather new volumes and save them to the database
# Scrape amazon's canadian website to read and register not (the latest prices), but common data (title, image, etc.) of berserk mangas to the API
class DataSpider(scrapy.Spider):
    limit = 0
    name = "datacrawler"
    allowed_domains = ["amazon.ca"]

    start_urls = [
        "https://www.amazon.ca/s/ref=sr_pg_3?rh=n%3A916520%2Ck%3ABerserk+volume&page=3&keywords=Berserk+volume&ie=UTF8&qid=1484536936"
    ]

    # Section is an amazon search result, which is a div within the HTML class s-tem-container
    def parse(self, response):
        for section in response.xpath('//div[@class="s-item-container"]'):
            item = AmazonItem()
            title = section.xpath('.//h2/text()').extract_first()
            # Substitute multiple whitespace with a single whitespace
            name = ' '.join(title.split())
            # ID is the volume's number / Gets extracted from the title then converted to an int
            product_id = ''.join(x for x in name if x.isdigit())

            # Scrapes if Format: Berserk Volume 16
            if name.startswith("Berserk Volume") and name[-1:].isdigit():
                item['name'] = name
                item['id'] = product_id

                date = section.xpath('.//span[3][contains(@class, "a-color-secondary")]/text()').extract_first()
                if len(date) > 4:
                    publication_date = datetime.datetime.strptime(date, '%b %d %Y').date()
                    item['publication_date'] = publication_date
                else:
                    item['publication_date'] = None

                image = section.xpath('.//img/@src').extract_first()
                if image:
                    item['image'] = image
                else:
                    item['image'] = None

                # Save to database
                item.save()

        # Crawl the next pages [limit = 4]
        next_page = response.xpath('//span[contains(@class, "pagnLink")]//a/@href').extract()
        if next_page and self.limit < 4:
            # If first page
            if self.limit == 0:
                next_page_url = next_page[0]
            else:
                next_page_url = next_page[1]
            self.limit += 1
            request = scrapy.Request(url="https://www.amazon.ca" + next_page_url)
            yield request
