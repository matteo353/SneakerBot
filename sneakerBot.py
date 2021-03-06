
import requests
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


df = pd.read_excel(r'/Users/matteo/Desktop/SneakerSpreadsheet.xlsx')

#function checks the availibility of product and returns url if present on site
#Definitely returns correct url if given the right input
def productChecker(website, nameOfProduct, size):

    websitelink = 'https://www.' + website + '/products.json'
    productData = requests.get(websitelink)

    #products gives us all products listed on given site
    products = json.loads((productData.text))['products']
    url = 'https://www.' + website + '/products/'

    for item in products:
        if (item['title'] == nameOfProduct):
            itemLink = url + item['handle']
            print(itemLink)
            checkoutBot(itemLink, size)
    return False
    


#pretty sure all shopify sites have the same backend syntax but have to check
#function to open url and checkout given shoe in selected size, ends at payment page
def checkoutBot(link, shoesize):

    #initializing web driver
    driver = webdriver.Chrome(ChromeDriverManager().install())

    #opening product page
    driver.get(link)

    #clicking on size of selected shoe
    sizeFormat = "'//div[@data-value=" + '"' + shoesize + '"' + "]'"
    print(sizeFormat)
    driver.find_element_by_xpath(sizeFormat).click()

    #clicking add to cart button and waiting for page to load
    driver.find_element_by_xpath('//button[@class="ffg productForm-submit js-productForm-submit"]').click()
    time.sleep(1)

    #clicking checkout button and waiting for page to load
    driver.find_element_by_xpath('//button[@class="button cart-checkout"]').click()
    time.sleep(1)

    #Filling in shipping info
    driver.find_element_by_xpath('//input[@placeholder="Email"]').send_keys("matteomastandrea1@gmail.com")
    driver.find_element_by_xpath('//input[@placeholder="First name"]').send_keys("Matteo")
    driver.find_element_by_xpath('//input[@placeholder="Last name"]').send_keys("Mastandrea")
    driver.find_element_by_xpath('//input[@placeholder="Address"]').send_keys("44 Example st")
    driver.find_element_by_xpath('//input[@placeholder="City"]').send_keys("Milton")
    driver.find_element_by_xpath('//input[@placeholder="ZIP code"]').send_keys("02186")

    #checking terms and conditions box
    driver.find_element_by_xpath('//input[@id="i-agree-terms__checkbox"]').click()

    #filling in phone number and hitting enter (the enter key: u'\ue007) / waiting for page to load
    driver.find_element_by_xpath('//input[@placeholder="Phone"]').send_keys("555-555-5555" + "\ue007")
    time.sleep(1)

    #clicking continue to payment button
    driver.find_element_by_xpath('//button[@class="step__footer__continue-btn btn"]').click()
    
    #ends at payment page


def functionManager(website, nameOfProduct, shoesize):
    if (productChecker(website, nameOfProduct) == False):
        print('Item not available')
        return
    else:
        link = productChecker(website, nameOfProduct)
        checkoutBot(link, shoesize)

#Getting the input of the product we're looking for and the website
productIndex = input("Product index: ")
website = input("Website name: ")

#Getting the name and size of the specified product
for index, row in df.iterrows():
    if index == productIndex:
        prodName = shoe['Name']
        size = shoe["BestSize']
                    
#Calling function manager to start the process with our new product information
functionManager(website, prodName, size)

                    
                    
