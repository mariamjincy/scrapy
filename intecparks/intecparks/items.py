# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IntecparksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	company_name = scrapy.Field()
	description = scrapy.Field()
	address = scrapy.Field()
	zip_code = scrapy.Field()
	city = scrapy.Field()
	website = scrapy.Field()
	email = scrapy.Field()
	phone = scrapy.Field()
