from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
chrome_driver_path = ""
url = "https://orteil.dashnet.org/cookieclicker//"

s = Service(chrome_driver_path)
driver = webdriver.Chrome(service = s)
driver.get(url)

cookie = driver.find_element(By.ID, "bigCookie")

items = driver.find_elements(By.CSS_SELECTOR, '#products div')
item_id = [item.get_attribute("id") for item in items[7::]]
item_ids = [item_id[i] for i in range(0, len(item_id), 7)]
print(item_ids)

def convert_money_to_int(money_element):
    money = len(money_element)
    mon = 0
    print(f'len recent:{money}')
    
    if money >= 26 and money < 28: #26,27
        mon = money_element.replace(money_element[3::],'')
        
    elif money == 25: #25
        mon = money_element.replace(money_element[2::],'')
        
    elif money <= 24: #(-oo, 24]
        mon = money_element.replace(money_element[1::],'')
        
    elif money >= 31 and money <=33: #31,32,33
        mon = money_element.replace(money_element[6::],'').replace(",", "")
        
    elif money == 29:
        mon = money_element.replace(money_element[4::],'').replace(",", "")
        
    elif money >= 28 or money == 30: #28,30
        mon = money_element.replace(money_element[5::],'').replace(",", "")
        
    elif money > 33:
        mon = money_element.replace(money_element[7::],'').replace(",", "")


    print(f'Recent Mon: {mon}')
    cookie_count = int(mon)
    print(f'Money {cookie_count}')
    #print(type(cookie_count))
    return cookie_count

def get_all_span(all_prices):
    item_prices = []
    for i in all_prices:
        element_text = i.text
        
        if element_text != "" and "," in element_text and " million" not in element_text :
            cost = int(element_text.replace(",", ""))
            item_prices.append(cost)
        elif element_text != "" and " million" in element_text:
            cost = element_text.replace(" million", "")
            cost = int( float(cost) ) * 1000000
            item_prices.append(cost)
        elif element_text != "":
            cost = int(element_text)
            item_prices.append(cost)
        else: 
            pass
    print(f'Item prices:{item_prices}')
    return item_prices

timeout = time.time() + 5
five_min = time.time() + 60*5# 5minutes
while True:
    cookie.click()

    #Every 5 seconds:
    if time.time() > timeout:
        
        #Get all upgrade <span> tags
        all_prices = driver.find_elements(By.CSS_SELECTOR,"#products span")
        item_prices = []
        
        #Convert <span> text into an integer price.
        item_prices = get_all_span(all_prices)
        
        #Create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]
            
        #Get current cookie count
        money_element = driver.find_element(By.XPATH,'//*[@id="cookies"]').text
        cookie_count = convert_money_to_int(money_element)

        #Find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                 affordable_upgrades[cost] = id
        print(f'affordable_upgrades:{affordable_upgrades}')

        #Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades) 
        print(f'Highest Price can buy: {highest_price_affordable_upgrade}')
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
        
        driver.find_element(By.ID, to_purchase_id).click()

        
        #Add another 20 seconds until the next check
        timeout = time.time() + 20
        
    #After 5 minutes stop the bot and check the cookies per second count.
    if time.time() > five_min:
        print('Process is Complete!!')
        break
