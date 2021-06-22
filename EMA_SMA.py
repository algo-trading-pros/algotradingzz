

import pandas as pd
from yahoo_fin import stock_info as si
import numpy as np

from matplotlib import pyplot as plt


import yfinance as yf

LARGEFONT =("Verdana", 35)

LARGEFONT =("Verdana", 35)
NORM_FONT =("Verdana", 15)
SMLL_FONT =("Verdana", 10)


stock = "RELIANCE"
DatCounter =9000

resampleSize = "5m"
DataPace = "1d"
candleWidth = 0.008
#defalut stock prise
s=5


def EMA_SMA(stock,s,now,resampleSize,DataPace):
	resampleSize = "5m"
	DataPace = "1d"

	# print("stock" , stock , "s" ,s , "time",now)

	#Interval required 5 minutes
	dataframe = yf.download(tickers=f"{stock}.ns", period=f"{DataPace}",  interval=f"{resampleSize}")

	#print(stock)

	df = dataframe.reset_index()


	df["Datetime"] = df['Datetime'].dt.tz_localize(None)

	df["EMA"]=df["Close"].ewm(span=10,adjust=False).mean()

	df["SMA"]=df["Close"].rolling(20).mean()

	df["SMA"].fillna( method ='ffill', inplace = True)
	df.dropna()

	df2 = df.iloc[[-1]]




	last_price = str(df2["Close"].values[0])

	start_date = "2021-06-21 10:15:00"
	after_start_date = df["Datetime"] >= now



	df = df.loc[after_start_date]

	# print(df)

	x = df['Datetime']
	f1 = df['EMA']
	g = df['SMA']
	idx = np.argwhere(np.diff(np.sign(f1 - g))).flatten()
	#print(np.sign(f - g))


	#print("printing idx \n" ,idx)
	idx1 = pd.DataFrame(np.sign(f1 - g))
	idx2 = idx1.dropna()
	#print(idx2)

	I = 0

	x = 0
	mid = 0


	global status_sell
	global status_sell1
	global message
	global invested
	global profit

	invested = " 0"
	profit = " 0"
	message = ""
	status_sell1 = ""
	status_sell = ""
	message = []
	if len(idx1.index) > 0 :
		x = idx1.index[0]
		while x <= idx1.index[-1]:
			if np.isnan(idx1.iat[x-idx1.index[0],0]) == False:
				#print(idx1.iat[x,0])
				#print(x)
				if idx1.iat[x-idx1.index[0],0] > 0 and mid == 0:
					I = I + df.at[x,'Close']*s
					mid += 1
					#print("Buying at" , u"\u20B9","%.2f" % df.at[x,'Close'] , " on " ,df.at[x,'Datetime'])
					#status_sell = str("Buying at" , "%.2f" % df.at[x,'Close'] ,df.at[x,'Datetime'])
					status_sell = "Buying at" + u"\u20B9" + str("%.2f" % df.at[x,'Close']) + " on " + str(df.at[x,'Datetime'])
					message.append(status_sell)
				elif idx1.iat[x-idx1.index[0],0] < 0 and mid == 1:
					I = I - df.at[x,'Close']*s
					mid -= 1
					#print("Seling at ", u"\u20B9" ,"%.2f" % df.at[x,'Close'], " on ",df.at[x,'Datetime'])
					#status_sell = str("Seling at " , "%.2f" % df.at[x,'Close'] , df.at[x,'Datetime'])
					status_sell1 = "Seling at " + u"\u20B9" + str("%.2f" % df.at[x,'Close']) + " on "+ str(df.at[x,'Datetime'])
					message.append(status_sell1)
			#print(I)
			#print(x)
			x = x + 1

		#global profit

		if mid == 0:

			profit = str("Profit/Loss " + str(I))
			#print("Profit/Loss " , I)
		elif mid ==1:

			profit = str(I - df.at[idx1[idx1[0].notnull()].index[0],'Close']*s)

			p = I - df.at[idx1[idx1[0].notnull()].index[0],'Close']*s
			#print("Profit/Loss " , p)

		#global invested
		invested = str(df.at[idx1[idx1[0].notnull()].index[0],'Close']*s)

	global waiting
	waiting = ""
	if len(idx1.index) == 0 :
		waiting = "BUY/SELL in PROGRESS... \n Waiting for EMA to cross SMA..."


	# print(status_sell)
	# print(status_sell1)
	#
	# print("profit" , profit)

	return [last_price , status_sell1 ,message ,invested , profit , waiting];

