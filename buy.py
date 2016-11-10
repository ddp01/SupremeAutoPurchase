# Colin Cowie and Kaaetech
import time
import sys
import requests
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
import time
import md5
import ConfigParser
from itertools import count

am = 2 # mode 2 will purchase keyword2 in the size2, and color2. mode1 will purchase both keyword2 and keyword.
done1 = False
done2 = False
config = ConfigParser.ConfigParser()
config.read('config.cfg')
product_name =  config.get('produkt', 'keyword')
product_color = config.get('produkt', 'color')
selectOption = config.get('produkt', 'size')
product_name2 =  config.get('produkt', 'keyword2')
product_color2 = config.get('produkt', 'color2')
selectOption2 = config.get('produkt', 'size2')
mainUrl = "http://www.supremenewyork.com/shop/all/" 
baseUrl = "http://supremenewyork.com"
checkoutUrl = "https://www.supremenewyork.com/checkout"
namefield = config.get('Info', 'Navn')
cat = config.get('produkt','cat')
cat2 = config.get('produkt','cat2')
emailfield = config.get('Info', 'Email')
phonefield = config.get('Info', 'Phone')
addressfield = config.get('Info', 'Addresse')
zipfield = config.get('Info', 'Zipfield')
countryfield = config.get('Info', 'Countryfield')
cityfield = config.get('Info', 'Cityfield')
cctypefield = config.get('Kreditkort', 'cctype') # "master" "visa" "american_express"
ccnumfield = config.get('Kreditkort', 'ccnum')  # cc nummer
ccmonthfield = config.get('Kreditkort', 'ccmonth') # maaned
ccyearfield = config.get('Kreditkort', 'ccyear') # udloebsaar
cccvcfield = config.get('Kreditkort', 'cvc')  # cvc
browser = Browser('chrome')


try:
    browser.visit(baseUrl)
    input("Tryk enter for at coppe!")
except SyntaxError:
    pass
start_time = time.time()

r = requests.get(mainUrl+cat).text
r2 = requests.get(mainUrl+cat2).text

def main():
    
   
    
    if am == 1 and product_name in r:
        print("Product1 Fundet")
        parse(r)
    if am == 2 and product_name2 in r2:
            print("Product2 Fundet")
            parser(r2)
    else:
        print(r)
        print("Product ikke fundet.")
        
def parser(r2):
    soup = BeautifulSoup(r2, "html.parser")
    for div in soup.find_all('div', { "class" : "inner-article" }):
        product = ""
        color = ""
        link = ""
        for a in div.find_all('a', href=True, text=True):
            link = a['href']
        for a in div.find_all(['h1','p']):
            if(a.name=='h1'):
                product = a.text
            elif(a.name=='p'):
                color = a.text
                
        checkproduct2(link,product,color)
        
def parse(r):
    soup = BeautifulSoup(r, "html.parser")
    for div in soup.find_all('div', { "class" : "inner-article" }):
        product = ""
        color = ""
        link = ""
        for a in div.find_all('a', href=True, text=True):
            link = a['href']
        for a in div.find_all(['h1','p']):
            if(a.name=='h1'):
                product = a.text
            elif(a.name=='p'):
                color = a.text
        checkproduct(link,product,color)



def checkproduct(Link,product_Name,product_Color):
    if(product_name in product_Name and product_color==product_Color):
        prdurl = baseUrl + Link
        print('\nPRODUKTET BLEV FUNDET\n')
        print('NAVN: '+product_Name+'\n')
        print('FARVE: '+product_Color+'\n')
        print('Link: '+prdurl+'\n')
        print('Naeste fase af koeb eller flere varer..\n')
        print('Product:'+product_Name+', Color:'+product_Color+', Link:'+Link)
        buyprd2(prdurl)
        
   
    
    
def checkproduct2(Link,product_Name,product_Color):
    if(product_name2 in product_Name and product_color2==product_Color):
        prdurl2 = baseUrl + Link
        print('\nPRODUKTET BLEV FUNDET\n')
        print('NAVN: '+product_Name+'\n')
        print('FARVE: '+product_Color+'\n')
        print('Link: '+prdurl2+'\n')
        print('Naeste fase af koeb eller flere varer..\n')
        buyprd(prdurl2)




def buyprd2(u):
        url = u
        browser.visit(url)
        browser.find_option_by_text(selectOption).first.click()
        browser.find_by_name('commit').click()
        if browser.is_text_present('item'):
            print("Added til kurven!")
            parser(r2)
            

        


def buyprd(u):
    url = u
    browser.visit(url)
    browser.find_option_by_text(selectOption2).first.click()
    browser.find_by_name('commit').click()
    if browser.is_text_present('item'):
        print("Added til kurven!")
    print("nu checkouter vi")
    time.sleep(0.1)
    browser.visit(checkoutUrl)
    print("udfylder dine Info")
    browser.fill("order[billing_name]", namefield)
    browser.fill("order[email]", emailfield)
    browser.fill("order[tel]", phonefield)

    print("udfylder din addrese")
    browser.fill("order[billing_address]", addressfield)
    browser.fill("order[billing_city]", cityfield)
    browser.fill("order[billing_zip]", zipfield)
    browser.select("order[billing_country]", countryfield)
    print("udfylder kort Info")
    browser.select("credit_card[type]", cctypefield)
    browser.fill("credit_card[cnb]", ccnumfield)
    browser.select("credit_card[month]", ccmonthfield)
    browser.select("credit_card[year]", ccyearfield)
    browser.fill("credit_card[vval]", cccvcfield)
    browser.find_by_css('.terms').click()
    print("betalt (maaske?) :)")
    print("--- %s sekunder ---" % (time.time() - start_time))
    browser.find_by_name('commit').click()

    quit()


i = 1

while (True):
    print("Forsoeg nummer " + str(i))
    main()
    i = i + 1
    time.sleep(1.75)
