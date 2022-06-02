import requests
from bs4 import BeautifulSoup
links=[]
i=1
for i in range(1,3):
    url = ('https://books.toscrape.com/catalogue/category/books/romance_8/page-'+str(i)+'.html')
    reponse = requests.get(url)
    #print(reponse)
    page = reponse.content
    soup = BeautifulSoup(page,"html.parser")
    titleBooks = soup.find_all('h3')
    for book in titleBooks:
        a=book.find('a')
        href='http://books.toscrape.com/catalogue/category/books/romance_8/'+a['href']
        links.append(href)
        
reponsePageBook = requests.get('https://books.toscrape.com/catalogue/chase-me-paris-nights-2_977/index.html')
pageBook = reponsePageBook.content
soup = BeautifulSoup(pageBook,"html.parser")
title = soup.find('h1')
#print(title.string)
titleBook=(title.string)
paragraph=soup.find_all('p')
description=paragraph[3].string
td=soup.find_all('td')
universal_product_code=td[0].string
price_including_tax=td[2].string
price_excluding_tax=td[3].string
number_available=td[5].string
review_rating=td[6].string
image=soup.find('img')
src_image='https://books.toscrape.com/catalogue/chase-me-paris-nights-2_977/'+image['src']