import nltk
from . import websearch
from difflib import SequenceMatcher
import pandas as pd
import spacy
import requests
from bs4 import BeautifulSoup as bs

nltk.download('stopwords')
nltk.download('punkt')
stop_words_en = set(nltk.corpus.stopwords.words('english')) 
nlp_uk = spacy.load('uk_core_news_sm')

def report(text, language='english'):
    matching_sites = web_verify(purify_text(text, language), 2)
    matches = {}

    for i in range(len(matching_sites)):
        matches[matching_sites[i]] = calculate_similarity(text, websearch.extractText(matching_sites[i]))

    matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}

    return matches

def purify_text(string, language='english'):
    if language == 'ukrainian':

        doc = nlp_uk(string)
        return " ".join([token.text for token in doc if not token.is_stop])
    else:

        words = nltk.word_tokenize(string)
        return " ".join([word for word in words if word.lower() not in stop_words_en])


def web_search_google(query, num_results):
    url = f'https://www.google.com/search?q={query}'
    results = []
    page = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}, timeout=10)
    soup = bs(page.text, 'html.parser')


    for link in soup.find_all('a'):
        url = link.get('href')
        if url.startswith('/url?q='):
            clean_url = url.split('/url?q=')[1].split('&')[0]
            if not any(excluded in clean_url for excluded in ['google.com', 'webcache.googleusercontent.com']):
                results.append(clean_url)

    return results[:num_results]

def web_verify(text, results_per_sentence):
    sentences = nltk.sent_tokenize(text)
    matching_sites = set()

    for url in web_search_google(query=text, num_results=results_per_sentence):
        matching_sites.add(url)

    for sentence in sentences:
        for url in web_search_google(query=sentence, num_results=results_per_sentence):
            matching_sites.add(url)

    return list(matching_sites)


def calculate_similarity(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio() * 100


def generate_report(text, language='english'):
    purified_text = purify_text(text, language)
    matching_sites = web_verify(purified_text, results_per_sentence=2)
    matches = {}

    for url in matching_sites:
        try:
            response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}, timeout=10)
            page_text = bs(response.text, 'html.parser').get_text()
            similarity = calculate_similarity(text, page_text)
            matches[url] = similarity
        except Exception as e:
            print(f"Error processing {url}: {e}")

    sorted_matches = dict(sorted(matches.items(), key=lambda item: item[1], reverse=True))
    return sorted_matches

def return_table(data):
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Similarity (%)'])
    return df.to_html()

if __name__ == '__main__':
    text_en = "This is a pure test"
    text_uk = "Це чистий тест"

    report_en = generate_report(text_en, language='english')
    report_uk = generate_report(text_uk, language='ukrainian')

    print("English Report:")
    print(return_table(report_en))
    print("Ukrainian Report:")
    print(return_table(report_uk))


# def purifyText(string, language='english'):
#     words = nltk.word_tokenize(string)
#     if language == 'ukrainian':
        
#         doc = nlp_uk(string)

#         return " ".join([token.text for token in doc if not token.is_stop])
#     else:
#         stop_words = stop_words_en
#     return " ".join([word for word in words if word.lower() not in stop_words])

# def webVerify(string, results_per_sentence):
#     sentences = nltk.sent_tokenize(string)
#     matching_sites = []
#     for url in websearch.searchBing(query=string, num=results_per_sentence):
#         matching_sites.append(url)
#     for sentence in sentences:
#         for url in websearch.searchBing(query = sentence, num = results_per_sentence):
#             matching_sites.append(url)

#     return (list(set(matching_sites)))

# def similarity(str1, str2):
#     return (SequenceMatcher(None,str1,str2).ratio())*100

# def report(text, language='english'):
#     matching_sites = webVerify(purifyText(text, language), 2)
#     matches = {}

#     for i in range(len(matching_sites)):
#         matches[matching_sites[i]] = similarity(text, websearch.extractText(matching_sites[i]))

#     matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}

#     return matches

# def returnTable(dictionary):

#     df = pd.DataFrame({'Similarity (%)': dictionary})
#     return df.to_html()

# if __name__ == '__main__':
#     report_en = report('This is a pure test', language='english')
#     report_uk = report('Це чистий тест', language='ukrainian')
    
#     print("English Report:", report_en)
#     print("Ukrainian Report:", report_uk)
