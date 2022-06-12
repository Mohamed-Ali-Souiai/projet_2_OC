import requests
from bs4 import BeautifulSoup
from math import ceil
import csv

def parserReponse(url):
    reponseCategory = requests.get(url)
    page = reponseCategory.content
    soup = BeautifulSoup(page,"html.parser")
    return soup

#page index de chaque categorie ==> parcourir tout les lien des categories
def pageIndexForCategory():
    ul=[]
    linksCategory=[]
    pageIndexCategory=[]

    url='http://books.toscrape.com/index.html'
    soup=parserReponse(url)
    ul = soup.find_all('ul')
    linksCategory = ul[2].find_all('a')

    for urlcat in linksCategory:
        adress='http://books.toscrape.com/'+urlcat['href']
        newUrl=adress.replace("index.html","")
        pageIndexCategory.append(newUrl)
        
    return pageIndexCategory

pageCategory=pageIndexForCategory()
# retourne le nombre de livre de chaque categorie 
def etlNumberOfBooks(link):
    soupNumberPage=parserReponse(link)
    strongNumberPage = soupNumberPage.find_all('strong')
    numberOfBooks=strongNumberPage[1].text
    return int(numberOfBooks)


# retourne nombre de page par categorie
def numberPagePerCategory(pageCat):
    
    numberPageCategory=[]
    #extraire les url des categories qui on 2 page ou plus
    nombreCategory=len(pageCat)
    for index in range(nombreCategory):
        NumberOfBooks = etlNumberOfBooks(pageCat[index])
        if NumberOfBooks>20:# 20==>nombre livrepar page NumberOfBooks==> nombre de livre/categorie
            numberPage = ceil(NumberOfBooks/20)
            numberPageCategory.append(numberPage)
        else:
            onePage=0
            numberPageCategory.append(0)
        
    return numberPageCategory

numPageCat=numberPagePerCategory(pageCategory)

# retourne url de livre de la categorie passer en parametre
def categoryBooks(t,npg,pageCat):
    links=[]

    if (npg[t])==0:
        url=pageCat[t]
        soupCategory=parserReponse(url)       
        titleBooks = soupCategory.find_all('h3')
        for book in titleBooks:
            a=book.find('a')
            href=url+a['href']
            links.append(href)
    else:
        for i in range(1,npg[t]+1):
            url=pageCat[t]+'page-'+str(i)+'.html'
            soupCategory=parserReponse(url)
            titleBooks = soupCategory.find_all('h3')
            for book in titleBooks:
                a=book.find('a')
                href=url+'../../'+a['href']
                links.append(href)
    return links


#les details des livres par categorie
t=len(pageCategory)-1 
donneeLivre=[]
entete=['category','product_page_url','title','product_description','universal_ product_code','price_including_tax',
        'price_excluding_tax','number_available','review_rating','image_url']
compteur=1 
for x in range(t+1): #pour parcourir tous les categories
    test=1
    y=len(categoryBooks(x,numPageCat,pageCategory)) 
    books = categoryBooks(x,numPageCat,pageCategory) 
    for z in range(y):  # pour parcourir tous les livres de la meme categorie

        url=books[z]
        soupBook=parserReponse(url)
        tc = soupBook.find_all('a')
        titleCategory=tc[3].text
        donneeLivre.append(titleCategory)

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
        with open(f'{titleCategory}_Book_{compteur}.jpg','wb') as f:
            f.write(reponseimg.content)

        #charge tous les details des livres par categories
        with open(f'etl_{titleCategory}.csv',"a",encoding='utf-8') as fichier:
            writer = csv.writer(fichier,delimiter=',')
            if test:
                writer.writerow(entete)
                test=0
            writer.writerow(donneeLivre)
        donneeLivre=[]
        compteur+=1 