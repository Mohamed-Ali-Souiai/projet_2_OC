import requests
from bs4 import BeautifulSoup
from math import *
import csv


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



#transformer ou prepare tous les Urls des categorie
def transformLinkPageCategory(): 
    
    pageIndexCategory=pageIndexForCategory() #contient tous les page index des categorie
    pageUrl=[]
    numberPageCategory=[]
    nombreCategory=len(pageIndexCategory)
    
    for index in range(nombreCategory):
        newUrl=pageIndexCategory[index].replace("index.html","")
        pageUrl.append(newUrl)  
    return pageUrl


# retourne le nombre de livre de chaque categorie 
def etlNumberOfBooks(link):
    urlNumberPage=link
    reponseNumberPage=requests.get(urlNumberPage)
    soupNumberPage = BeautifulSoup(reponseNumberPage.content,'html.parser')
    strongNumberPage = soupNumberPage.find_all('strong')
    numberOfBooks=strongNumberPage[1].text
    return int(numberOfBooks)


# retourne nombre de page par categorie
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


# retourne url de livre de la categorie passer en parametre
def categoryBooks(t):
    links=[]
    linkTransform=transformLinkPageCategory()
    nombrePage=numberPagePerCategory() #tous les numbres de page de chaque categorie en ordre avec transformLinkPageCategory()

    if (nombrePage[t])==0:
        url=linkTransform[t]   
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


#retoune liste de tous les titres de categorie
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



#les details des livres par categorie
t=len(pageIndexForCategory())-1 
donneeLivre=[]
entete=['category','product_page_url','title','product_description','universal_ product_code','price_including_tax',
        'price_excluding_tax','number_available','review_rating','image_url']
compteur=1 
for x in range(t+1): #pour parcourir tous les categories
    test=1
    y=len(categoryBooks(x)) 
    books = categoryBooks(x) 

    extracTitleCategory = extractTitleCategory()
    titleCategory=extracTitleCategory[x] 

    for z in range(y):  # pour parcourir tous les livres de la meme categorie
        donneeLivre.append(titleCategory)

        url=books[z]        
        reponsePageBook = requests.get(url)
        pageBook = reponsePageBook.content
        soupBook = BeautifulSoup(pageBook,"html.parser")

        donneeLivre.append(url)

        title = soupBook.find('h1')
        titleBook=title.string
        donneeLivre.append(titleBook)

        paragraph=soupBook.find_all('p')
        description=paragraph[3].string
        donneeLivre.append(description)

        td=soupBook.find_all('td')
        universal_product_code=td[0].string
        donneeLivre.append(universal_product_code)


        price_including_tax=td[2].string 
        donneeLivre.append(price_including_tax)

        price_excluding_tax=td[3].string  
        donneeLivre.append(price_excluding_tax)

        number_available=td[5].string
        donneeLivre.append(number_available)    

        review_rating=td[6].string   
        donneeLivre.append(review_rating)

        image=soupBook.find('img')
        src_image=url+'../../'+image['src']
        donneeLivre.append(src_image)

        #charge les images
        reponseimg=requests.get(src_image)
        with open('images/book'+titleCategory+str(compteur)+'.jpg','wb') as f:
            f.write(reponseimg.content)

        #charge tous les details des livres par categories
        with open("etl"+titleCategory+".csv","a",encoding='utf-8') as fichier:
            writer = csv.writer(fichier,delimiter=',')
            if test:
                writer.writerow(entete)
                test=0
            writer.writerow(donneeLivre)
        donneeLivre=[]
        compteur+=1 