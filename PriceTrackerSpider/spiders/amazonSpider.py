import re
import scrapy
import datetime
from PriceTrackerSpider.items import AmazonItem


# Scrape amazon's canadian website to read and register the latest prices of berserk mangas to the API
class AmazonSpider(scrapy.Spider):
    limit = 0
    name = "amazon"
    allowed_domains = ["amazon.ca"]

    start_urls = [
        # Shorten this link
        "https://www.amazon.ca/s/ref=nb_sb_ss_i_2_6?url=search-alias%3Dstripbooks&field-keywords=berserk+manga"
    ]

    # Section is an amazon search result, which is a div within the HTML class s-tem-container
    def parse(self, response):
        for section in response.xpath('//div[@class="s-item-container"]'):
            item = AmazonItem()
            title = section.xpath('.//h2/text()').extract_first()
            # Substitute multiple whitespace with a single whitespace
            name = ' '.join(title.split())

            # Scrapes if Format: Berserk Volume 16
            if name.startswith("Berserk Volume") and name[-1:].isdigit():
                item['name'] = name

                # ID is the volume's number / Gets extracted from the title then converted to an int
                item['id'] = int(''.join(x for x in title if x.isdigit()))

                date = section.xpath('.//span[3][contains(@class, "a-color-secondary")]/text()').extract_first()
                if len(date) > 4:
                    publication_date = datetime.datetime.strptime(date, '%b %d %Y').date()
                    item['publication_date'] = publication_date
                else:
                    item['publication_date'] = None

                cost = section.xpath('.//span[contains(@class, "s-price")]/text()').extract_first()
                if cost:
                    # Remove CAD$ from the price
                    price = re.sub('[CDN$]', '', cost)
                    item['price'] = float(price)
                else:
                    item['price'] = None

                image = section.xpath('.//img/@src').extract_first()
                if image:
                    item['image'] = image
                else:
                    item['image'] = None

                store_link = section.xpath('.//a/@href').extract_first()
                if store_link:
                    item['store_link'] = store_link
                else:
                    item['store_link'] = None

                availability = section.xpath('.//div[contains(@class, "a-span7")]//div[4]//span/text()').extract_first()
                if availability:
                    item['availability'] = availability
                else:
                    item['availability'] = "Not sold by Amazon.ca"
                # Return for json
                # yield item
                # Save to database
                yield item

        # Crawl the next pages [limit = 3]
        next_page = response.xpath('//span[contains(@class, "pagnLink")]//a/@href').extract()
        if next_page and self.limit < 4:
            # If first page
            if self.limit == 0:
                next_page_url = next_page[0]
            else:
                next_page_url = next_page[1]
            self.limit += 1
            request = scrapy.Request(url="https://www.amazon.ca"+next_page_url)
            yield request
