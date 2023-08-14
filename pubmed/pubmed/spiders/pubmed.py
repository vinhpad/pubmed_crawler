from scrapy import Spider
from scrapy.selector import Selector
import sys
class CrawlerSpider(Spider):
    name = "pubmed"
    allowed_domains = ["pubmed.ncbi.nlm.nih.gov"]
    start_urls = [
        "https://pubmed.ncbi.nlm.nih.gov/31501885/",
    ]

    def parse(self, response):

        abstract = Selector(response).xpath('//div[@class="abstract"]/div/p/text()')
        print("=================")
        print(abstract)
        print("=================")
        words = ""
        for sentence in abstract:
            words = words + sentence.get()


        # original_stdout = sys.stdout
        # with open('demo.txt', 'w') as f:
        #     sys.stdout = f  # Change the standard output to the file we created.
        #     print(words)
        #     sys.stdout = original_stdout  # Reset the standard output to its original value
        #print(response)
        paper_id = response.css('div.docsum-content').extract()
        print(paper_id)
        #print(f'paper id = {paper_id}')
        #yield from response.follow_all('https://pubmed.ncbi.nlm.nih.gov/' + , callback=self.parse)
