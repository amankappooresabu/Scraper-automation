from typing import Any
import scrapy

class BayutSpider(scrapy.Spider):

    name = 'bayut_spider'
    allowed_domains = ['bayut.bh']
    start_urls = ['https://www.bayut.bh/en/to-rent/commercial/bahrain/']

    def parse(self, response):
        property_urls = response.xpath('//a[@aria-label="Listing link"]/@href').getall()
        property_urls = list[Any](set[Any](property_urls))  
        self.logger.info(f'Found {len(property_urls)} unique property URLs on this page')
        
        for url in property_urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.parse_property)
        
    def parse_property(self, response):
          yield {
            'reference_number': response.xpath('//span[@aria-label="Reference"]/text()').get(),  
            'id': response.xpath('substring-after(//span[@aria-label="Reference"]/text(), "ID")').get(),
            'url': response.url, 
            'purpose': response.xpath('//span[@aria-label="Purpose"]/text()').get(), 
            'title': response.xpath('//h1[@class="_4bbafa79 fontCompensation"]/text()').get(),  
            'description': ' '.join(response.xpath('//span[@class="_812d3f30"]/text()').getall()),  
            'location': response.xpath('//div[@aria-label="Property header"]/text()').get(),  
            'price': response.xpath('//span[@aria-label="Price"]/text()').get(),
            'currency': response.xpath('//span[@aria-label="Currency"]/text()').get(),
            'price_per': response.xpath('//span[@aria-label="Frequency"]/text()').get(), 
            'furnished': response.xpath('//span[@aria-label="Furnishing"]/text()').get(),
            'amenities': ','.join(response.xpath('//div[@class="_050edc8e"]/following-sibling::div//span[@class="c0327f5b"]/text()').getall()),
        }