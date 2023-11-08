import pandas
import requests
from bs4 import BeautifulSoup
from metadata import *
from tqdm import tqdm
from preprocess import preprocess
from sklearn.model_selection import ShuffleSplit
import numpy
from multiprocessing import Process

class DataAugment(object):
    def __init__(self, task, domain, pubmed_id_name_colums, max_level, crawl_limit, batch_size, output):
        data_frame = pandas.read_csv(domain, index_col= False)
        self.task = task
        self.pubmed_ids = data_frame[pubmed_id_name_colums]
        self.max_level = max_level
        self.visted_pubmed_id = dict()
        self.total_crawler_link = []
        self.limit = crawl_limit
        self.batch_size = batch_size
        self.output = output


    def __crawler_similar_articles(self, level, pubmed_id):
        try:
            if(len(self.total_crawler_link) > self.limit):
                return

            self.visted_pubmed_id[pubmed_id] = True
            self.total_crawler_link.append(pubmed_id)
            self.__crawler_abstract_pubmed(url=DOMAIN_LINK+str(pubmed_id))

            if level == self.max_level:
                return
        
            response = requests.request("GET",
                                DOMAIN_LINK + str(pubmed_id),
                                headers=HEADER,
                                data=PAYLOAD)
            
            soup = BeautifulSoup(response.text, 'html.parser')

            similar_articles = soup.select('#similar-articles-list > li > div > a')

            for similar_article in similar_articles:
                pubmed_id_child = similar_article["data-ga-action"]
                if self.visted_pubmed_id.get(pubmed_id_child) is None:
                    self.__crawler_similar_articles(level + 1, pubmed_id_child)
        except Exception as exception:
            print(exception)

    def __crawler_abstract_pubmed(self, url):
        response = requests.request("GET",
                            url,
                            headers=HEADER,
                            data=PAYLOAD)
    
        soup = BeautifulSoup(response.text, 'html.parser')        
        list_ = soup.select("#eng-abstract > p")
        date_raw = soup.select('#full-view-heading > div > div > span')
        date_raw = date_raw[1].text
        year = date_raw[0] + date_raw[1] + date_raw[2] + date_raw[3]

        abstract = ""
        for i in list_:
            if abstract != "":
                abstract = abstract + " " + preprocess(i.text)
            else:
                abstract = preprocess(i.text)
        if abstract != "":
            with open(self.output ,'a+') as csv_file:
                csv_file.write("{}|{}|{}\n".format(url, abstract, year))

    def crawl_per_batch(self, pubmed_ids):
        for pubmed_id in tqdm(pubmed_ids):
            if self.visted_pubmed_id.get(pubmed_id) is None:
                self.__crawler_similar_articles(level=0, pubmed_id=pubmed_id)
        print(f'Task {self.task} get total {len(self.total_crawler_link)} paper')

    def run(self):
        pubmed_ids_list = numpy.array_split(self.pubmed_ids, self.batch_size)
        for pubmed_ids in tqdm(pubmed_ids_list):
            self.crawl_per_batch(pubmed_ids=pubmed_ids)
            #sub_process = Process(target=self.crawl_per_batch, args=(self, pubmed_ids))
            #sub_process.start()