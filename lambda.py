import math
import random
import yfinance as yf
import pandas as pd
from datetime import date, timedelta
from pandas_datareader import data as pdr
# override yfinance with pandas – seems to be a common step
yf.pdr_override()

# Get stock data from Yahoo Finance – here, asking for about 10 years of Amazon
today = date.today()
print(today)
decadeAgo = today - timedelta(days=3652)
print(decadeAgo)

data = pdr.get_data_yahoo('AMZN', start=decadeAgo, end=today) 
# Other symbols: CSCO – Cisco, NFLX – Netflix, INTC – Intel, TSLA - Tesla 
print(data)

# Add two columns to this to allow for Buy and Sell signals
# fill with zero
data['Buy']=0
data['Sell']=0


# Find the 4 different types of signals – uncomment print statements
# if you want to look at the data these pick out in some another way
for i in range(len(data)): 
    # Hammer
    realbody=math.fabs(data.Open[i]-data.Close[i])
    bodyprojection=0.1*math.fabs(data.Close[i]-data.Open[i])

    if data.High[i] >= data.Close[i] and data.High[i]-bodyprojection <= data.Close[i] and data.Close[i] > data.Open[i] and data.Open[i] > data.Low[i] and data.Open[i]-data.Low[i] > realbody:
        data.at[data.index[i], 'Buy'] = 1
        #print("H", data.Open[i], data.High[i], data.Low[i], data.Close[i])   

    # Inverted Hammer
    if data.High[i] > data.Close[i] and data.High[i]-data.Close[i] > realbody and data.Close[i] > data.Open[i] and data.Open[i] >= data.Low[i] and data.Open[i] <= data.Low[i]+bodyprojection:
        data.at[data.index[i], 'Buy'] = 1
        #print("I", data.Open[i], data.High[i], data.Low[i], data.Close[i])

    # Hanging Man
    if data.High[i] >= data.Open[i] and data.High[i]-bodyprojection <= data.Open[i] and data.Open[i] > data.Close[i] and data.Close[i] > data.Low[i] and data.Close[i]-data.Low[i] > realbody:
        data.at[data.index[i], 'Sell'] = 1
        #print("M", data.Open[i], data.High[i], data.Low[i], data.Close[i])

    # Shooting Star
    if data.High[i] > data.Open[i] and data.High[i]-data.Open[i] > realbody and data.Open[i] > data.Close[i] and data.Close[i] >= data.Low[i] and data.Close[i] <= data.Low[i]+bodyprojection:
        data.at[data.index[i], 'Sell'] = 1
        #print("S", data.Open[i], data.High[i], data.Low[i], data.Close[i])




# Data now contains signals, so we can pick signals with a minimum amount
# of historic data, and use shots for the amount of simulated values
# to be generated based on the mean and standard deviation of the recent history
no_resource=2
Open=[]
High=[]
Low=[]
Close=[]
Adj_Close=[]
Volume=[]
Buy=[]
Sell=[]


for i in data['Open']:
    Open.append(i)

for i in data['High']:
    High.append(i)

for i in data['Low']:
    Low.append(i)

for i in data['Close']:
    Close.append(i)

for i in data['Adj Close']:
    Adj_Close.append(i)

for i in data['Volume']:
    Volume.append(i)

for i in data['Buy']:
    Buy.append(i)

for i in data['Sell']:
    Sell.append(i)

minhistory = 100
shots = 1000000
def getpage(Close,minhistory,shots):
    try: 
        host = "zlvaz80q08.execute-api.us-east-1.amazonaws.com" 
        c = http.client.HTTPSConnection(host) 
        data = {
        "Q":Close,
        "D":minhistory,
        
        "S":shots
        } 
        c.request("POST", "/default/course_work", json.dumps(data)) 
        response = c.getresponse() 
        print("AWS response",response)
        data = json.loads(response.read().decode('utf-8'))
        #data.update({"Resource_id":id})
        print( data)
        return data 
    except IOError: 
        print( 'Failed to open ', host ) # Is the Lambda address correct? 
        print(data+" from "+str(id)) # May expose threads as completing in a different order 
        return "page "+str(id)
 
def getpages(matching,shots,rate,runs): 
    with ThreadPoolExecutor() as executor: 
        #results=executor.map(getpage, runs)
        
        
        for i in runs:
            data=getpage(i,int(matching),int(shots),int(rate))
            print("getpage_data",data)
            results.append(data)
    return results
def do_something(Close,minhistory,shots,Buy,no_resource):
    parallel = no_resource
    runs=[value for value in range(parallel)]
    print("there")
    getpages(matching,shots,rate,runs)
    
 
 
    for result in results: 
        print("the resulstnd sdkj",result)
 
    
    return results