import json
import pandas
import requests
from bs4 import BeautifulSoup
import re
import string
import unicodedata
import viet_text_tools
from tqdm import tqdm
from vncorenlp import VnCoreNLP
url = "https://pubmed.ncbi.nlm.nih.gov/9951474/"

#rdrsegmenter = VnCoreNLP("../vncorenlp/VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx5g')



size_giay = []
size_quan_ao = []

def preprocess(text):
    text = str(text)
    text = unicodedata.normalize("NFC", text)
    text = viet_text_tools.normalize_diacritics(text)
    text = remove_emoji(text)
    #text = text.lower()
    # text = re.sub(r'(\[[^]]*])', " ", text)
    # text = re.sub(r'(\([^)]*\))', " ", text)
    # text = re.sub(r'(<[^>]*>)', " ", text)
    # text = re.sub(f'[{string.punctuation}³]', " ", text)
    # text = re.sub(r'\b([a-z]+)([0-9]+)([a-z]*)\b', " ", text)
    # text = re.sub('’', " ", text)
    # text = re.sub('‘', " ", text)
    # text = re.sub('“', " ", text)
    text = re.sub('\n', " ", text)
    text = re.sub('\t', " ", text)
    text = re.sub("\r", " ", text)
    text = " ".join(text.split())
    #text = word_segment(text)
    # text = re.sub(r'\b([0-9]+)\b', " ", text)
    text = ' '.join(text.split())
    return text




def remove_emoji(s):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', s)

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

file = open('CPR.json')
data = json.load(file)
urls = data.keys()
id = []
abstracts = []

for url in  tqdm(urls):
    response = requests.request("GET", "https://pubmed.ncbi.nlm.nih.gov/" +  url, headers=headers, data=payload)

    soup = BeautifulSoup(response.text, 'html.parser')
    list_ = soup.select("#eng-abstract > p")
    abstract = ""

    for i in list_:
      if abstract != "":
        abstract = abstract + " " + preprocess(i.text)
      else:
        abstract = preprocess(i.text)
    id.append([url, abstract])
    if len(id) % 10 == 0 :
        dataframe = pandas.DataFrame(id, columns=['id', 'abstract'])
        dataframe.to_csv('CPRaug.csv', index=False)

dataframe = pandas.DataFrame(id, columns=['id', 'abstract'])
dataframe.to_csv('CPRaug.csv', index=False)