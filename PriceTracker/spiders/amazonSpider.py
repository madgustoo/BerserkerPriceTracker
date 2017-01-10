import re
import scrapy
from PriceTracker.items import AmazonItem


# Scrape amazon's canadian website to read and register the latest prices of berserk mangas to the API
class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.ca"]

    start_urls = [
        # Shorten this link
        "https://www.amazon.ca/s/ref=nb_sb_ss_i_1_7?url=search-alias%3Dstripbooks&field-keywords=berserk&sprefix=berserk%2Caps%2C140&crid=2EQUOUQ7COBVX"
    ]

    def parse(self, response):
        # Section is a <li></li> amazon search result
        for section in response.xpath('//*[@id="s-results-list-atf"]//li')
            item = AmazonItem()
            # https://doc.scrapy.org/en/latest/topics/selectors.html
            item['name'] = section.xpath('.//h2/text()').extract();
            # item['price'] = response.xpath('//*[@id="result_0"]/div/div/div/div[2]/div[3]/div[1]/div[2]/a/span[2]/text()').extract()
            # item['publication_date'] = response.xpath('//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/span[3]/text()').extract()
            # item['image'] = response.xpath('//*[@id="result_0"]/div/div/div/div[1]/div/div/a/img/@src').extract()
            # item['availability'] = response.xpath('//*[@id="result_0"]/div/div/div/div[2]/div[3]/div[1]/div[4]/span/text()').extract()
            # item['store_link'] = response.xpath('//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/a/@href').extract()
            yield item
