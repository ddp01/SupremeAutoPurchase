#Created by Colin Cowie - CFG and tweak by kaaetech  
import time
import sys
import requests
from bs4 import BeautifulSoup
from splinter import Browser
import time
import md5
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.cfg')
product_name =  config.get('produkt', 'keyword')
product_color = config.get('produkt', 'color')
selectOption = config.get('produkt', 'size')
mainUrl = "http://www.supremenewyork.com/shop/all/accessories"
baseUrl = "http://supremenewyork.com"
checkoutUrl = "https://www.supremenewyork.com/checkout"
namefield = config.get('Info', 'Navn')
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
    input("Tryk enter for at coppe!")
except SyntaxError:
    pass
start_time = time.time()



def main():
    
    r = requests.get(mainUrl).text
    #print(r)
    if product_name in r:
        print("Product Fundet")
        parse(r)
    else:
        print("Product ikke fundet.")

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
        print('Naeste fase af koeb..\n')
        buyprd(prdurl)
    #print('Product:'+product_Name+', Color:'+product_Color+', Link:'+Link)




def buyprd(u):
   
    url = u
    browser.visit(url)
  
    # 10|10.5
    browser.find_option_by_text(selectOption).first.click()
    browser.find_by_name('commit').click()
    if browser.is_text_present('item'):
        print("Added til kurven!")
    else:
        print("Out of stock.")
        return
    print("nu checkouter vi")
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
    time.sleep(1)

