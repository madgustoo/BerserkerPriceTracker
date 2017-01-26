import scrapy
import datetime
from PriceTrackerSpider.items import AmazonItem
from .util import strip_whitespace


# This Spider will run once a month, at the end of each to gather new volumes and save them to the database
# Scrape amazon's canadian website to read and register not (the latest prices), but common data (title, image, etc.) of berserk mangas to the API
class DataSpider(scrapy.Spider):
    limit = 0
    name = "datacrawler"
    allowed_domains = ["amazon.ca"]

    start_urls = [
        "https://www.amazon.ca/s/ref=sr_pg_1?rh=n%3A916520%2Ck%3ABerserk+volume&keywords=Berserk+volume&ie=UTF8&qid=1484711680"
    ]

    # Section is an amazon search result, which is a div within the HTML class s-tem-container
    def parse(self, response):
        for section in response.xpath('//div[@class="s-item-container"]'):
            item = AmazonItem()
            title = section.xpath('.//h2/text()').extract_first()
            # Substitute multiple whitespace with a single whitespace
            name = strip_whitespace(title)
            # ID is the volume's number / Gets extracted from the title then converted to an int
            product_id = ''.join(x for x in name if x.isdigit())

            # Scrapes if Format: Berserk Volume 16
            if name.startswith("Berserk Volume") and name[-1:].isdigit() and len(name) < 20:
                item['name'] = name
                item['id'] = product_id

                date = section.xpath('.//span[3][contains(@class, "a-color-secondary")]/text()').extract_first()
                if date and len(date) > 4:
                    publication_date = datetime.datetime.strptime(date, '%b %d %Y').date()
                    item['publication_date'] = publication_date

                image = section.xpath('.//img/@src').extract_first()
                if image:
                    item['image'] = image

                # Save to database
                item.save()

        # Crawl the next pages [limit = 3]
        next_page = response.xpath('//span[contains(@class, "pagnLink")]//a/@href').extract()
        if next_page and self.limit < 3:
            # If first page
            if self.limit == 0:
                next_page_url = next_page[0]
            else:
                next_page_url = next_page[1]
            self.limit += 1
            request = scrapy.Request(url="https://www.amazon.ca" + next_page_url)
            yield request
