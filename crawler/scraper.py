import scrapy
from bs4 import BeautifulSoup

class BlogSpider(scrapy.Spider):
    name = 'spider'
    start_urls = ['https://onepiece.fandom.com/wiki/Devil_Fruit']

    def parse(self, response):
        for href in response.css('navibox toccolours mw-collapsible mw-made-collapsible')[0].css("a::attr(href)").extract():
            extracted_data = scrapy.Request("https://onepiece.fandom.com"+href,
                           callback=self.parse_jutsu)
            yield extracted_data

        for next_page in response.css('a.mw-nextlink'):
            yield response.follow(next_page, self.parse)
    
    def parse_jutsu(self, response):
        category = response.css("span.mw-page-title-main::text").extract()[0]
        category = category.strip()

        div_selector = response.css("div.mw-parser-output")[0]
        div_html = div_selector.extract()

        soup = BeautifulSoup(div_html).find('div')

        title=""
        if soup.find('aside'):
            aside = soup.find('aside')

            for cell in aside.find_all('div',{'class':'pi-data'}):
                if cell.find('h3'):
                    cell_name = cell.find('h3').text.strip()
                    if cell_name == "Classification":
                        title = cell.find('div').text.strip()

        soup.find('aside').decompose()

        text = soup.text.strip()
        text = text.split('Trivia')[0].strip()

        return dict (
            category = category,
            title = title,
            text = text
        )