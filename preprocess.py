from vncorenlp import VnCoreNLP
import viet_text_tools
import re
import unicodedata

def preprocess(text):
    text = str(text)
    text = unicodedata.normalize("NFC", text)
    text = viet_text_tools.normalize_diacritics(text)
    text = remove_emoji(text)
    text = text.lower()
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