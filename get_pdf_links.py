import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

paperlist = []

subject = str(input("Enter maths, science, english, chinese or tamil") or "%")
level = str(input("Enter P1 to P6, or leave blank for all levels") or "%")
year = str(input("Enter 2000 to 2020, or leave blank for all years") or "%")
exam_type = str(input("Enter CA1, CA2, SA1, SA2 or leave blank for all exam types") or "%")

def numberOfPages(subject, level, year, exam_type):
    url = f'https://www.testpapersfree.com/{subject}/index.php?level={level}&year={year}&subject={subject}&type={exam_type}&school=%&Submit=Show%20Test%20Papers&page=1'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    pages = soup.find_all('div',{'class':'table-wrapper'})
    page = pages[1]
    try:
        numberofpage = page.find_all('a')
        numberofpages = int(numberofpage[-2].text)
    except:
        numberofpages = 1
    return numberofpages

numberofpages = numberOfPages(subject, level, year, exam_type)

def getPapers(subject, level, year, exam_type, page):
    url = f'https://www.testpapersfree.com/{subject}/index.php?level={level}&year={year}&subject={subject}&type={exam_type}&school=%&Submit=Show%20Test%20Papers&page={page}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.find_all('table')
    table = tables[1]

    for quest in table.find_all('a'):
        link = quest.get('href')
        if link.startswith('../'):
            paper={
            'name': quest.text,
            'link': 'https://www.testpapersfree.com/' + link.rsplit('/',1)[1]
            }
            paperlist.append(paper)

i = 1
while i <= numberofpages:
    getPapers(subject, level, year, exam_type, i)
    i+=1
    
df = pd.DataFrame(paperlist)

df.to_excel('test_papers.xlsx')
print(paperlist)
