import scrapy


class ShopSpidey(scrapy.Spider):
    name = 'shop_spidey'
    start_urls = [f"https://spettroworld.com/shop/product/page/{i}" for i in range(1, 28)]

    def parse(self, response):
        for href in list(set(response.css('h5.mkd-product-list-title a ::attr("href")').extract())):
            yield response.follow(href, self.parse_product)

    def parse_product(self, response):
        def extract_summary():
            information = {
                'name': response.css('h3.mkd-single-product-title::text').get(),
                'price': response.css('p.price span::text').get(),
                'description': " ".join([x.get() for x in response.css('div.summary div p::text')]).replace(u'\xa0', u' '),
                'size_guide': "\n".join([x.get() for x in response.css('div.size-guide::text')])
            }
            for count, image_url in enumerate(response.css('div.thumbnails a::attr(href)').extract()):
                information[f'image_url_{count + 1}'] = image_url
            return information
        return extract_summary()

