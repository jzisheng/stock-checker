import requests
from datetime import datetime
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


DEBUG = False

driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub",
                          DesiredCapabilities.CHROME)


d = json.load(open('/home/zisheng/botkeys.json'))
DISCO_NJ_CHANNEL = d['DISCO_NJ_CHANNEL']
DISCO_VA_CHANNEL = d['DISCO_VA_CHANNEL']
TEST_CHANNEL = d['TEST_CHANNEL']
NJ_URL = d['NJ_URL']
VA_URL = d['VA_URL']

def sendMessage(disco_hook,msg):
    myobj = {'content': msg}
    x = requests.post(disco_hook, json = myobj)
    print(x)


def checkStock(disco_hook,url):
    driver.get(url)    
    prodNames = driver.find_elements_by_xpath("//*[starts-with(@id, 'hypProductH2')]")
    stockAmt = driver.find_elements_by_xpath("//*[starts-with(@class, 'stock')]")
    videoCards = driver.find_elements_by_xpath("//*[starts-with(@data-category, 'Video Cards')]")
    if len(videoCards) == 0:
        print("[bot]:",len(videoCards),"in stock")
        return "Out of stock"
    
    stocks = []
    for sn in stockAmt:
        stocks.append(sn.text)
    names = []
    for p in prodNames:
        names.append(p.text)
    
    res = (list(zip(names,stocks)))
    tot = []
    
    for prod, stockStr in res:
        if "IN STOCK" in stockStr:
            ss = ["-"*10,prod,"**"+stockStr+"**"]
            tot.append("\n".join(ss))
    if tot:
        tot = tot[:3]
        tot.append("[Microcenter website]({})".format(url))
        msg = ("\n".join(tot))
        print(msg)
        sendMessage(disco_hook, msg)

    return "In stock"

def genUrl(url_str,keywords):
    return url_str.format("+".join(keywords))


def main():
    if DEBUG == False:
        keywords = ["rtx","3080"]    
        checkStock(DISCO_NJ_CHANNEL, genUrl(NJ_URL,keywords))
        checkStock(DISCO_VA_CHANNEL, genUrl(VA_URL,keywords))    

        keywords = ["rtx","3060"]
        checkStock(DISCO_NJ_CHANNEL, genUrl(NJ_URL,keywords))    
        checkStock(DISCO_VA_CHANNEL, genUrl(VA_URL,keywords))    

    else:
        keywords = ["gtx","1060"]    
        checkStock(TEST_CHANNEL, genUrl(NJ_URL,keywords))

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time, "Checked Stock")

try:
    main()
except:
    print("[bot]: error occured")
    sendMessage(TEST_CHANNEL,"[bot]: error occured")
driver.quit()
