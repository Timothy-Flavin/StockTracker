import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
import time
from datetime import datetime
import SMS
from email.mime.text import MIMEText

def getStockPrice(query):
    my_results_list = ""
    urls=search(query+" ticker yahoo finance",        # The query you want to run
                    tld = 'com',  # The top level domain
                    lang = 'en',  # The language
                    num = 5,     # Number of results per page
                    start = 0,    # First result to retrieve
                    stop = 5,  # Last result to retrieve
                    pause = 2.0,  # Lapse between HTTP requests
                )
    for i in urls:
        my_results_list = my_results_list +i
    #print(my_results_list)

    regexList =[r"finance\.yahoo\.com/[a-z]+/[A-Z]+[/?%,\.]", r"p=[A-Z]+"]
    #regexList[0]: looking for finance.yahoo.com/quote or chart/ticker ending in some other gibberish
    #regexList[1]: looking for p= Capital word to catch the ones that end in p=Ticker. This one may not be needed
    rTickerList = [r"/[A-Z]+[/?%,]$", r"[A-Z]+$"]
    #these pull the tickers out of the matched string
    trimList =[(1,-1),(0,'')]
    #these trom the list but I am not sure how to do the 
    yahooLink = None
    i=-1
    while (yahooLink is None) and (i<len(regexList)-1):
        i=i+1
        #print(i)
        yahooLink = re.search(regexList[i], my_results_list)
        
    
    if yahooLink != None:
        ticker = yahooLink.group()
        #print(ticker)
        #print(str(trimList[i][0])+":"+str(trimList[i][1]))
        try:
            ticker = re.search(rTickerList[i], ticker).group()
            ticker = ticker[trimList[i][0]:-1 if trimList[i][1] is not '' else len(trimList)]
            print("Company name: "+query+", Ticker Symbol: "+ticker, end=', current price: $')
        #ticker = input()
            url = "https://finance.yahoo.com/quote/%s/"%(ticker)
            for j in range(3):
                try:
                    r = requests.get(url)
                except ValueError:
                    print("Request failed, will try "+str(2-i)+" more times\n"+ValueError)
            soup = BeautifulSoup(r.text,'html.parser')
            stockPrice = soup.find_all('div', {'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
            if len(stockPrice) >0:
                print(stockPrice)
                return(ticker, stockPrice)
            else:
                print('error finding the stock price')
                return(0,0)
        except:
            print("error finding the ticker from yahoo link")
    else:
        print("no yahoo finance link found for " + query)
        return (0,0)

print("enter mail username")
usrnm = input()
print("enter mail password")
pswrd = input()
print("enter phone number (no '-' or spaces ex:1112223333)")
phoneNumber = input()

PreviousCheck = {}

while(True):
    
    print("####### Updating stock prices based on file 'StockData.txt'. #######")
    print("Current time: " + str(datetime.now()))

    startSystemTime = time.perf_counter()

    textFile = open('StockData.txt', 'r').read()
    #print(textFile)
    try:
        textFile = re.findall(r"<[\w\d:]+>", str(textFile))
        #print("Text File: ")
        
        for i in range(len(textFile)):
            textFile[i] = textFile[i][1:-1]
        #print(textFile)
        schedulingMethod = textFile[0]
        if(schedulingMethod.lower() == 'interval'):
            try:
                intervalWaitTime = int(textFile[1])
            except:
                print("Could not get wait time, file improperly formatted")
        else:
            print("not yet implemented time of day scheduling")
        
        queryList = list()
        stockRanges = list()
        for i in range(2,len(textFile),2): #first 2 will need to change for time scheduling
            #print("did this work? "+str(i))
            queryList.append(textFile[i])
            if queryList[len(queryList)-1] not in PreviousCheck:
                PreviousCheck[queryList[len(queryList)-1]] = False
            stockRanges.append(textFile[i+1].split(':'))
            #print(stockRanges)
            #print(int((i-2)/2))
            if stockRanges[int((i-2)/2)][0].isnumeric():
                stockRanges[int((i-2)/2)][0] = float(stockRanges[int((i-2)/2)][0])
            if stockRanges[int((i-2)/2)][1].isnumeric() or stockRanges[int((i-2)/2)][1] == 'inf':
                stockRanges[int((i-2)/2)][1] = float(stockRanges[int((i-2)/2)][1])
            else:
                print("Stock price ranges not numeric")
        stockResults = list()
        print(stockRanges)
        print(PreviousCheck)
        messageToSend = '\nDate and time, '+str(datetime.now()) +'\n'
        messageToSend = messageToSend+"Stocks within range:\n"
        stockEnteredAcceptedRange = False
        for i in range(len(queryList)):
            stockResults.append(getStockPrice(queryList[i]))
            if (stockRanges[i][0] < float(stockResults[i][1]) < stockRanges[i][1]) and PreviousCheck[queryList[i]] is False:
                messageToSend = messageToSend+str(queryList[i])+", "+str(stockResults[i]) +'\n'
                stockEnteredAcceptedRange = True
                PreviousCheck[queryList[i]]=True
            else:
                print(queryList[i]+"Not Within designated Range or already notified")
        #print("==============RESULTS================")
        #print(stockResults)
        #print(messageToSend)
        #print(PreviousCheck)
        #print("==============END=RESULTS============")
        #input()
        if stockEnteredAcceptedRange:
            print("text me")
            SMS.send(messageToSend, phoneNumber,usrnm,pswrd)
    except ValueError:
        print(str(ValueError)+ "could not properly decode 'StockData.txt'. Is the file missing or poorly formatted?")

    timeElapsed = time.perf_counter() - startSystemTime
    print("Time Elapsed Finding Prices: "+ str(timeElapsed)+" seconds.")
    print("Time until next Update: "+ str((intervalWaitTime*60-timeElapsed)/60) + " minutes")
    print("####################################################################")
    print()
    time.sleep(intervalWaitTime*60-timeElapsed)