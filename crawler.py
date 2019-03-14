import scrapy;

class CSSUngoliant(scrapy.Spider):
    name = 'lotrCrawler'
    start_urls = ['https://lotr.fandom.com/wiki/Category:Characters']

    def parse(self, response):
        for keyword in response.css('.category-page__members > ul > li a::attr(href)'):
            yield response.follow(keyword, self.parseDetails)
        for href in response.css('.category-page__pagination a::attr(href)'):
            yield response.follow(href, self.parse)
    
    def parseDetails(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        
        yield {
            'name': extract_with_css('h1.page-header__title ::text'),
            'details': extract_with_css('#mw-content-text > p')
                .replace('href="', 'target="_blank" href="https://lotr.fandom.com'),
            'url': response.request.url,
            'thumbnail': extract_with_css('.pi-image .pi-image-thumbnail::attr(src)'),
            'race': extract_with_css('.pi-data[data-source = "race"] .pi-data-value ::text'),
            'gender': extract_with_css('.pi-data[data-source = "gender"] .pi-data-value ::text'),
            'culture': extract_with_css('.pi-data[data-source = "culture"] .pi-data-value ::text')
        }