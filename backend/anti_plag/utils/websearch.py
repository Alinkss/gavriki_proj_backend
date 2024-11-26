import requests
from bs4 import BeautifulSoup as bs
import warnings

warnings.filterwarnings("ignore", module='bs4')


def searchGoogle(query, num):
    url = f'https://www.google.com/search?q={query}'
    urls = []
    
    page = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}, timeout=10)
    page.encoding = 'utf-8'
    soup = bs(page.text, 'html.parser')

    for link in soup.find_all('a'):
        url = str(link.get('href'))

        if url.startswith('/url?q='):
            clean_url = url.split('/url?q=')[1].split('&')[0]
            if not any(excluded in clean_url for excluded in ['google.com', 'webcache.googleusercontent.com']):
                urls.append(clean_url)

    return urls[:num]

# def searchBing(query, num):

#     url = 'https://www.bing.com/search?q=' + query
#     urls = []

#     page = requests.get(url, headers = {'User-agent': 'Mozilla/5.0'}, timeout=10)
#     page.encoding = 'utf-8'
#     soup = bs(page.text, 'html.parser')

#     for link in soup.find_all('a'):
#         url = str(link.get('href'))
#         if url.startswith('http'):
#             if not url.startswith('http://go.m') and not url.startswith('https://go.m'):
#                 urls.append(url)
    
#     return urls[:num]

def extractText(url):
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    return " ".join([p.get_text() for p in soup.find_all('p')])