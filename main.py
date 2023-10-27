import json
import pandas
import requests
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
headers = {
  'authority': 'pubmed.ncbi.nlm.nih.gov',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'en-US,en;q=0.9',
  'cache-control': 'max-age=0',
  'cookie': 'pm-csrf=kZ8FJE03phv9SQb0KKoJipXL8kmx1BU4DdHptUamgVYfKYZ1i7ta7nlRFXxDMOOS; pm-sessionid=vbj3ak38pgi92mxpdbwqzc938vmmufg5; ncbi_sid=D69A00A64DC7EFC3_0133SID; _gid=GA1.2.729464156.1692172111; _gat_ncbiSg=1; _gat_dap=1; _ga_DP2X732JSX=GS1.1.1692172111.1.0.1692172111.0.0.0; _ga=GA1.1.1931705388.1692172111; ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgGIFEBs+ADCQIxH67YAiAggMICsJJAzKQBz4Dse+pATgAsHAHSlRAWziMQAGhABXAHYAbAPYBDVMqgAPAC6ZQAJkzhFAI0lR0C1ubBWbdkEPObLAZwMRNAYyMFWSx5EBMicz5iMgoqOiYWInYuXgJBEXEpGTCTUkdnWwwnayLPHz9AjAA5AHlq3FyzLBKXUWV/S2R21Ul25ERRAHN1GFyBc0EIsNZIrHIOSPt8+YFp+2aQBaWQVgcsADNNVS8oGfcsX0Uz+w5zGYmsDlJuWQUhOZABViEzd/2QERRKwxH83BclGotDp9EE3CFAWFGADSKx8G8QIwIeRkkj8OZ0UjuOZ3Ap+OZGKRSSBCOZoL5kLAbjS7lgBAJKUJuO4AL48oA===; ncbi_sid=D69A00A64DC7EFC3_0133SID; pm-csrf=kZ8FJE03phv9SQb0KKoJipXL8kmx1BU4DdHptUamgVYfKYZ1i7ta7nlRFXxDMOOS; pm-sessionid=vbj3ak38pgi92mxpdbwqzc938vmmufg5',
  'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}
(chemicals ,genes ) = load_chemicals_genes()
visited = dict()

for url in  tqdm(urls):
    if visited.get(url) == True:
       continue
    try:
      visited[url] = True
      response = requests.request("GET", "https://pubmed.ncbi.nlm.nih.gov/" +  url, headers=headers, data=payload)

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