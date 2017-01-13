# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from volume.models import Product


class AmazonItem(DjangoItem):
    django_model = Product


class TestItem(scrapy.Item):
    name = scrapy.Field()
    id = scrapy.Field()
    price = scrapy.Field()
    publication_date = scrapy.Field()
    image = scrapy.Field()
    availability = scrapy.Field()
    store_link = scrapy.Field()
