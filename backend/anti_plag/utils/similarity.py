import nltk
from . import websearch
from difflib import SequenceMatcher
import pandas as pd
import spacy

nltk.download('stopwords')
nltk.download('punkt')
stop_words_en = set(nltk.corpus.stopwords.words('english')) 
nlp_uk = spacy.load('uk_core_news_sm')

def purifyText(string, language='english'):
    words = nltk.word_tokenize(string)
    if language == 'ukrainian':
        
        doc = nlp_uk(string)

        return " ".join([token.text for token in doc if not token.is_stop])
    else:
        stop_words = stop_words_en
    return " ".join([word for word in words if word.lower() not in stop_words])

def webVerify(string, results_per_sentence):
    sentences = nltk.sent_tokenize(string)
    matching_sites = []
    for url in websearch.searchBing(query=string, num=results_per_sentence):
        matching_sites.append(url)
    for sentence in sentences:
        for url in websearch.searchBing(query = sentence, num = results_per_sentence):
            matching_sites.append(url)

    return (list(set(matching_sites)))

def similarity(str1, str2):
    return (SequenceMatcher(None,str1,str2).ratio())*100

def report(text, language='english'):
    matching_sites = webVerify(purifyText(text, language), 2)
    matches = {}

    for i in range(len(matching_sites)):
        matches[matching_sites[i]] = similarity(text, websearch.extractText(matching_sites[i]))

    matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}

    return matches

def returnTable(dictionary):

    df = pd.DataFrame({'Similarity (%)': dictionary})
    return df.to_html()

if __name__ == '__main__':
    report_en = report('This is a pure test', language='english')
    report_uk = report('Це чистий тест', language='ukrainian')
    
    print("English Report:", report_en)
    print("Ukrainian Report:", report_uk)
