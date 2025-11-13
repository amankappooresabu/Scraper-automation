# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BayutPipeline:
    def process_item(self, item, spider):
      
        
        if item.get('amenities'):
            amenities_list = item['amenities'].split(',')
            seen = set()
            cleaned_amenities = []
            for amenity in amenities_list:
                amenity = amenity.strip()
                if amenity and amenity not in seen:
                    seen.add(amenity)
                    cleaned_amenities.append(amenity)
            item['amenities'] = ','.join(cleaned_amenities)
        
        if item.get('price'):
            item['price'] = item['price'].replace(',', '')
        
        for key, value in item.items():
            if isinstance(value, str):
                item[key] = value.strip()
        
        return item
