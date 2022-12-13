import os
import scrapy 
from scrapy.loader import ItemLoader
from ..items import AmazonxItem
from scrapy.crawler import CrawlerProcess
from scrapy import Request

class AmazonxItem(scrapy.Spider):

    name = 'amazonmobile'
    allowed_domains = ['amazon.in']
    start_urls = ['https://www.amazon.in/a-href/s?k=mobile']
    custom_settings = {"FEEDS": {"results2.csv": {"format": "csv"}},'CONCURRENT_REQUESTS': 1}
    headers = {
        'user-agent' :
        'User-Agent: Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'
        }
    
    try:
        os.remove('results.csv')
    except OSError:
        pass

    def start_requests(self):
        url = 'https://www.amazon.in/a-href/s?k=mobile'
        print(url)
        yield scrapy.Request(url= url, headers= self.headers, callback= self.parse)         
       
    def parse(self, response):
        file = open("wh.html", "wb")
        file.write(response.text.encode('utf-8'))
        file.close()
        all_mobiles = response.xpath('//div[@class="a-section a-spacing-small a-spacing-top-small"]//h2')
        for mobile in all_mobiles:
            details_link = mobile.xpath('.//a/@href').get()
            absolute_url = response.urljoin(details_link)   

            link = mobile.xpath('.//a/@href').get()
            link = f"https://www.amazon.in{link}"
            product_name = mobile.xpath('.//a/span/text()').get()
            

            yield Request(absolute_url, callback= self.fetch_detail, meta={'link': link, 'product_name':product_name})            
    
        #pagination logic shifted
        next_page = response.xpath('//span[@class="s-pagination-item s-pagination-selected"]//following-sibling::a[@aria-label="Go to page 2"]/@href').get()
        # print(next_page)
        if next_page:
            abs_url = f"https://www.amazon.in{next_page}" #https://www.amazon.in/mobile/s?k=mobile&page=2
            print(abs_url)
            yield response.follow(url= abs_url , callback=self.parse)    
 
    def fetch_detail(self,response):
        link = response.meta.get('link')
        product_name = response.meta.get('product_name')
        mobile_name = response.xpath('//h1[@id="title"]/span/text()').get() 
        mobile_price = response.xpath('//div[@id="corePriceDisplay_desktop_feature_div"]//span[@class="a-price-whole"]/text()').getall() 
        customer_rating = response.xpath('//span[@data-hook="rating-out-of-text"]//text()').get()
        yield{'link': link, 'product_name' : product_name, 'mobile_name':mobile_name, 'mobile_price': mobile_price, 'customer_rating': customer_rating} 
    


            

        
    
