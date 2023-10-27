import pandas
import requests
from bs4 import BeautifulSoup
from metadata import HEADER, PAYLOAD, DOMAIN_LINK
from tqdm import tqdm
DATA_DOMAIN_PATH = "domain_task/chemprot_training_abstracts.tsv"

data = pandas.read_csv(DATA_DOMAIN_PATH, index_col=False)
pubmed_ids = data["Pubmed_ID"]
visted_pubmed_id = dict()

total_crawler_link = []


def crawler_similar_articles(level, pubmed_id):
    visted_pubmed_id[pubmed_id] = True
    total_crawler_link.append(pubmed_id)
    if level == 3:
        return

    res = requests.request("GET",
                           f'{DOMAIN_LINK}{pubmed_id}',
                           headers=HEADER,
                           data=PAYLOAD)
    soup = BeautifulSoup(res.text, 'html.parser')
    similar_articles = soup.select('#similar-articles-list > li > div > a')
    for similar_article in similar_articles:
        pubmed_id_child = similar_article["data-ga-action"]
        if visted_pubmed_id.get(pubmed_id_child) is None:
            crawler_similar_articles(level + 1, pubmed_id_child)


for pubmed_id in tqdm(pubmed_ids):
    # print(pubmed_id)
    crawler_similar_articles(level=0, pubmed_id=pubmed_id)
    if len(total_crawler_link) % 100 == 0:
        dataframe = pandas.DataFrame(total_crawler_link, columns=['pubmed_id'])
        dataframe.to_csv('CPR_id_aug.csv', index=False)
print(f'Total link crawler {len(total_crawler_link)}')
