import requests
from bs4 import BeautifulSoup
from math import *
import csv


#details de chaque livre
t=1
y=0
#def detailsBooks():
category = categoryBooks(t) # le parametre t correspond aux classements des categories c'est pour parcourir tous les categories
titleCategory = extractTitleCategory()
url=category[y]             # y correspond au page de category en cours
reponsePageBook = requests.get(url)
pageBook = reponsePageBook.content
soupBook = BeautifulSoup(pageBook,"html.parser")

title = soupBook.find('h1')
titleBook=title.string

paragraph=soupBook.find_all('p')
description=paragraph[3].string

td=soupBook.find_all('td')
universal_product_code=td[0].string
price_including_tax=td[2].string
price_excluding_tax=td[3].string
number_available=td[5].string
review_rating=td[6].string

image=soupBook.find('img')
src_image=url+'../../'+image['src'] 
    


def categoryBooks(t):
    links=[]
    linkTransform=transformLinkPageCategory()
    nombrePage=numberPagePerCategory() #tous les numbres de page des categorie en ordre avec transformLinkPageCategory()

    if (nombrePage[t])==0:
        url=linkTransform[t]    #ici je n'ai pas ajouté "index.html" alors que url fonctionne
        reponse=requests.get(url)
        page=reponse.content
        soupCategory=BeautifulSoup(page,"html.parser")
        titleBooks = soupCategory.find_all('h3')
        for book in titleBooks:
            a=book.find('a')
            href=url+a['href']
            links.append(href)
    else:
        for i in range(1,nombrePage[t]+1):
            url=linkTransform[t]+'page-'+str(i)+'.html'
            reponse=requests.get(url)
            page=reponse.content
            soupCategory=BeautifulSoup(page,"html.parser")
            titleBooks = soupCategory.find_all('h3')
            for book in titleBooks:
                a=book.find('a')
                href=url+'../../'+a['href']
                links.append(href)
    
    return links




#page index de chaque categorie ==> parcourir tout les lien des categories
def pageIndexForCategory():
    ul=[]
    linksCategory=[]
    pageIndexCategory=[]

    url='http://books.toscrape.com/index.html'
    reponseCategory = requests.get(url)
    pageCategory = reponseCategory.content
    soup = BeautifulSoup(pageCategory,"html.parser")
    ul = soup.find_all('ul')
    linksCategory = ul[2].find_all('a')

    for urlcat in linksCategory:
        adress='http://books.toscrape.com/'+urlcat['href']
        pageIndexCategory.append(adress)
        
    return pageIndexCategory
#pageIndexForCategory()

def extractTitleCategory():
    linkCategory=pageIndexForCategory()
    titleCategory=[]
    for link in linkCategory:
        reponse=requests.get(link)
        page=reponse.content
        soup=BeautifulSoup(page,'html.parser')
        title=soup.find('h1').text
        titleCategory.append(title) 
    return titleCategory



#def etlCategoryBooks(linksCategory):#le lien de chaque livre ==> parcourir tout les lien des livre
def transformLinkPageCategory(): #transformer tous les liens des categorie
    
    pageIndexCategory=pageIndexForCategory() #contient tous les page index des categorie
    pageUrl=[]
    numberPageCategory=[]
    nombreCategory=len(pageIndexCategory)
    
    for index in range(nombreCategory):
       
        newUrl=pageIndexCategory[index].replace("index.html","")
        pageUrl.append(newUrl)
        
    return pageUrl


def numberPagePerCategory():
    
    pageIndexCategory=pageIndexForCategory() #contient tous les page index des categorie
    numberPageCategory=[]
    #extraire les url des categories qui on 2 page ou plus
    nombreCategory=len(pageIndexCategory)
    for index in range(nombreCategory):
        NumberOfBooks = etlNumberOfBooks(pageIndexCategory[index])
        if NumberOfBooks>20:# 20==>nombre livrepar page NumberOfBooks==> nombre de livre/categorie
            numberPage = ceil(NumberOfBooks/20)
            numberPageCategory.append(numberPage)

        else:
            onePage=0
            numberPageCategory.append(0)
        
    return numberPageCategory


def etlNumberOfBooks(link):#le nombre des livres de chaque categorie 
    urlNumberPage=link
    reponseNumberPage=requests.get(urlNumberPage)
    soupNumberPage = BeautifulSoup(reponseNumberPage.content,'html.parser')
    strongNumberPage = soupNumberPage.find_all('strong')
    numberOfBooks=strongNumberPage[1].text
    return int(numberOfBooks)
#print(etlNumberOfBooks(PIC[12]))

    