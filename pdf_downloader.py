import requests
import sys
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
import wget
from urllib.request import urlopen
import urllib.request 
import pandas as pd

data = pd.read_excel('test_papers.xlsx')

hdrs = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def get_pdfs(my_url):
    for url in my_url:
        links = []
        filenames = []
        html = requests.get(url).text
        html_page = bs(html, features="lxml")
        base = urlparse(url)
        print("base",base)
        for link in html_page.find_all('a'):
            current_link = link.get('href')
            if current_link.endswith('pdf'):
                filenames.append(current_link.rsplit('/',1)[1])
                links.append(base.scheme + "://" + base.netloc + "/" + current_link)
                print(links)
                print(filenames)
                
        for link in links:
            i=0
            r = requests.get(link)
            with open (str(filenames[i]),'wb') as f:
                 f.write(r.content)
            i+=1


def main():
    print("Enter Link: ")
    my_url = data.link.tolist()
    get_pdfs(my_url)

main()

