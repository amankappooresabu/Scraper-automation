from typing import Any
import scrapy

class BayutSpider(scrapy.Spider):

    name = 'bayut_spider'
    allowed_domains = ['bayut.bh']
    start_urls = ['https://www.bayut.bh/en/to-rent/commercial/bahrain/']
    item_count = 0
    max_items = 1050

    def parse(self, response):
        property_urls = response.xpath('//a[@aria-label="Listing link"]/@href').getall()
        property_urls = list(set(property_urls))
        self.logger.info(f'Found {len(property_urls)} unique property URLs on this page')
        
        for url in property_urls:
            if self.item_count >= self.max_items:
               self.logger.info(f'Reached {self.max_items} items limit. Stopping.')
               return
            self.item_count += 1
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.parse_property)
        next_page = response.xpath('//a[@title="Next" and not(@disabled)]/@href').get()
    
        if next_page and self.item_count < self.max_items:
           next_page_url = response.urljoin(next_page)
           self.logger.info(f'Following next page: {next_page_url}')
           yield scrapy.Request(next_page_url, callback=self.parse)
        else:
           self.logger.info('No more pages or reached item limit')
        
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
            'amenities': ','.join(response.xpath('//span[@class="c0327f5b"]/text()').getall()),
            'details': response.xpath('//span[@aria-label="Area"]//span/text()').get(),
            'agent_name': response.xpath('//span[@aria-label="Agent name"]/text()').get(),
            'number_of_photos': str(len(response.xpath('//div[@aria-label="Gallery dialog photo grid"]//source[@type="image/webp"]/@srcset').getall())),
            'breadcrumb': ' > '.join([response.xpath('normalize-space(//div[@aria-label="Breadcrumb"]/div/text())').get()] + response.xpath('//div[@aria-label="Breadcrumb"]//span[@aria-label="Link name"]/text()').getall()),
            'property_image_urls': response.xpath('//div[@aria-label="Gallery dialog photo grid"]//source[@type="image/webp"]/@srcset').getall(),
            'property_type': response.xpath('//span[@aria-label="Type"]/text()').get(), 
            } 