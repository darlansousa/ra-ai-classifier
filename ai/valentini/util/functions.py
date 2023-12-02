import pandas as pd
import nltk
from unidecode import unidecode
from nltk.corpus import stopwords

stop_words = set(stopwords.words('portuguese'))


def concat_filter(row):
    if pd.notnull(row['title']) and pd.notnull(row['description']):
        return f"{row['title']}. {row['description']}"

    if pd.notnull(row['title']):
        return f"{row['title']}"

    if pd.notnull(row['description']):
        return f"{row['description']}"

    return None


def replace_words(text_messages):
    processed = text_messages.str.replace(r'^.+@[^\.].*\.[a-z]{2,}$', 'emailaddress')
    processed = processed.str.replace(
        r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+['
        r'a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})',
        'webaddress')
    processed = processed.str.replace(
        r'[\$\xA2-\xA5\u058F\u060B\u09F2\u09F3\u09FB\u0AF1\u0BF9\u0E3F\u17DB\u20A0-\u20BD\uA838\uFDFC\uFE69\uFF04'
        r'\uFFE0\uFFE1\uFFE5\uFFE6]',
        'moneysymb')

    processed = processed.str.replace(r'^\([1-9]{2}\) (?:[2-8]|9[0-9])[0-9]{3}\-[0-9]{4}$',
                                      'phonenumbr')
    processed = processed.str.replace(r'\d+(\.\d+)?', 'numbr')
    processed = processed.str.replace(r'[^\w\d\s]', ' ')
    processed = processed.str.replace(r'\s+', ' ')
    processed = processed.str.replace(r'^\s+|\s+?$', '')
    processed = processed.apply(unidecode)
    processed = processed.str.lower()
    return processed


def remove_stop_words(text):
    return text.apply(lambda x: ' '.join(term for term in x.split() if term not in stop_words))


def stem_words(text):
    ps = nltk.stem.RSLPStemmer()
    return text.apply(lambda x: ' '.join(ps.stem(term) for term in x.split()))


def formatting(df):
    df["docs"] = df.apply(concat_filter, axis=1)
    text = replace_words(df["docs"])
    text = remove_stop_words(text)
    text = stem_words(text)
    return text
