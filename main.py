import json
import pandas
import requests
from metadata import HEADER, PAYLOAD
from bs4 import BeautifulSoup
from preprocess import preprocess
from tqdm import tqdm
from vncorenlp import VnCoreNLP
from get_chemical_gene import load_chemicals_genes

url = "https://pubmed.ncbi.nlm.nih.gov/9951474/"

file = open('CPR.json')
data = json.load(file)
urls = data.keys()
id = []
abstracts = []
payload={}
(chemicals ,genes ) = load_chemicals_genes()
visited = dict()

for url in  tqdm(urls):
    if visited.get(url) == True:
       continue
    try:
      visited[url] = True
      response = requests.request("GET", "https://pubmed.ncbi.nlm.nih.gov/" +  url, headers=HEADER, data=PAYLOAD)

      soup = BeautifulSoup(response.text, 'html.parser')
      list_ = soup.select("#eng-abstract > p")
      date_raw = soup.select('#full-view-heading > div > div > span')
      date_raw = date_raw[1].text
      date = date_raw[0] + date_raw[1] + date_raw[2] + date_raw[3]
      
      abstract = ""

      for i in list_:
        if abstract != "":
          abstract = abstract + " " + preprocess(i.text)
        else:
           abstract = preprocess(i.text)

        chemicals_in_abstract = []
        genes_in_abstract = []
        for chemical in chemicals:
           chemical = chemical.lower()
           if abstract.find(chemical) != -1:
              chemicals_in_abstract.append(chemical)

        for gene in genes:
           gene = gene.lower()
           if abstract.find(gene) != -1:
              genes_in_abstract.append(gene)

        id.append([url, abstract, date , chemicals_in_abstract, genes_in_abstract])
        

        if len(id) % 10 == 0 :
           dataframe = pandas.DataFrame(id, columns=['id', 'abstract', 'year', 'chemicals', 'genes'])
           dataframe.to_csv('CPRaug.csv', index=False)
    except Exception as exception:
       print(f'[ERROR:] {exception}')
dataframe = pandas.DataFrame(id, columns=['id', 'abstract'])
dataframe.to_csv('CPRaug.csv', index=False)