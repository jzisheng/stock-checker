import requests
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

DEBUG = True

driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub",
                          DesiredCapabilities.CHROME)
# driver = webdriver.Chrome('/usr/local/bin/chromedriver')

d = json.load(open('/Users/zisheng/botkeys.json'))
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
    
    stocks = []
    for sn in stockAmt:
        stocks.append(sn.text)
    names = []
    for p in prodNames:
        names.append(p.text)
    
    res = (list(zip(names,stocks)))
    tot = []
    
    for prod, stockStr in res:
        if "IN STOCK" in stockStr: #  or DEBUG:
            ss = ["-"*10,prod,"**"+stockStr+"**"]
            tot.append("\n".join(ss))
    if tot:
        tot = tot[:3]
        tot.append("[Microcenter website]({})".format(url))
        msg = ("\n".join(tot))
        sendMessage(disco_hook, msg)

def genUrl(url_str,keywords):
    return url_str.format("+".join(keywords))



if DEBUG == False:
    keywords = ["rtx","3060"]    
    checkStock(DISCO_NJ_CHANNEL, genUrl(NJ_URL,keywords))   
else:
    keywords = ["intel","i7"]    
    checkStock(TEST_CHANNEL, genUrl(NJ_URL,keywords))
driver.quit()
