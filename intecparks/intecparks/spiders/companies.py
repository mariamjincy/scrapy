# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from intecparks.items import IntecparksItem

class CompaniesSpider(scrapy.Spider):
	name = 'companies'
	allowed_domains = ['intecparks.com']
	start_urls = ['http://www.intecparks.com/no_cache/kerala-it/it-companies-in-kerala/?tx_wtdirectory_pi1%5Bpointer%5D=0']
	BASE_URL = 'http://www.intecparks.com'
	HEADERS = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate',
			'Accept-Language':'en-US,en;q=0.8,ml;q=0.6',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

	def parse(self, response):
		DETAILS_SELECTOR_XPATH = '//ul[@class="wtdirectory_list wtdirectory_list_wrap"]/li'
		COMPANY_XPATH = './/dt[contains(b/text(),"Company")]/following-sibling::dd/h2/text()'
		DESCRIPTION_XPATH = './/dt[contains(b/text(),"Description")]/following-sibling::dd[1]//text()'
		ADDRESS_XPATH = './/dt[contains(b/text(),"Address")]/following-sibling::dd//text()'
		ZIP_CODE_XPATH = './/dt[contains(b/text(),"ZIP Code")]/following-sibling::dd//text()'
		CITY_XPATH = './/dt[contains(b/text(),"City")]/following-sibling::dd//text()'
		WEBSITE_XPATH = './/dt[contains(b/text(),"Homepage address")]/following-sibling::dd//a/@href'
		EMAIL_XPATH = './/dt[contains(b/text(),"Email Address")]/following-sibling::dd/a/text()'
		PHONE_XPATH = './/dt[contains(b/text(),"Phone")]/following-sibling::dd//text()'
		NEXT_PAGE_XPATH = '//ul[@class="wt_directory_pagebrowser"]/li[contains(a/@class,"act")]/following-sibling::li[1]/a/@href'

		if response.xpath(DETAILS_SELECTOR_XPATH):
			for i in response.xpath(DETAILS_SELECTOR_XPATH):
				company = i.xpath(COMPANY_XPATH).extract()
				description = i.xpath(DESCRIPTION_XPATH).extract()
				address = i.xpath(ADDRESS_XPATH).extract()
				zip_code = i.xpath(ZIP_CODE_XPATH).extract()
				city = i.xpath(CITY_XPATH).extract()
				website = i.xpath(WEBSITE_XPATH).extract()
				email = i.xpath(EMAIL_XPATH).extract()
				phone = i.xpath(PHONE_XPATH).extract()

				company = company[0].strip() if company else ''
				description = ' '.join(''.join(description).split()) if description else ''
				address = address[0].strip() if address else ''
				zip_code = zip_code[0].strip() if zip_code else ''
				city = city[0].strip() if city else ''
				website = website[0].strip() if website else ''
				email = email[0].strip().replace('[at]','@') if email else ''
				phone = phone[0].strip() if phone else ''

				item = IntecparksItem(
					company_name = company,
					description=description,
					address=address,
					zip_code=zip_code,
					city=city,
					website=website,
					email=email,
					phone=phone,
					)
				yield item

			next_page = response.xpath(NEXT_PAGE_XPATH).re('(.*)&cHash')
			next_page = self.BASE_URL+'/'+next_page[0] if next_page else ''
			if next_page:
				yield Request(next_page,callback =self.parse,headers=self.HEADERS)


