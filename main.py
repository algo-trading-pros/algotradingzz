import tkinter
import tkinter as tk
from tkinter import Frame, ttk
#from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.animation as animation
# from matplotlib import style
import pandas as pd
from yahoo_fin import stock_info as si
import numpy as np
from threading import Thread
import profit_loss
import ratio_exit
from tkinter import PhotoImage
import time_dependend

from matplotlib import style
from matplotlib import pyplot as plt
# import matplotlib.dates as mdates
# import matplotlib.ticker as mticker
#
# import  mplfinance as mpl
# from mplfinance.original_flavor import candlestick_ohlc
# import matplotlib.dates as mpl_dates

import yfinance as yf

import tkinter.scrolledtext as tkst
# import time

LARGEFONT =("Verdana", 35)
style.use("ggplot")
LARGEFONT =("Verdana", 35)
NORM_FONT =("Verdana", 15)
SMLL_FONT =("Verdana", 10)

f = plt.figure()
#a = f.add_subplot(111)

stock = "RELIANCE"
DatCounter =9000

resampleSize = "5m"
DataPace = "1d"
candleWidth = 0.008
s=0

def makeAThread(function):
    Thread(target = function).start()

def changeTimeFrame(tf):
	global DataPace
	global DatCounter
	DataPace = tf
	if tf == "7d" and resampleSize == "1m" :
		popupmsg("Too much data chosen,choose a smaller time frame or higher OHLC interval")
	else :
		DataPace = tf
		#DatCounter = 9000
	print(DataPace)

def changeSampleSize(size,width) :
	global resampleSize
	global candleWidth
	resampleSize = size
	if DataPace == "7d" and resampleSize == "1m" :
		popupmsg("Too much data choseen , choose a smaller time frame and higher OHLC interval")

	else :
		#resampleSize = size
		DatCounter = 9000
		candleWidth =width
	print(resampleSize)

def popupmsg(msg):
	popup = tk.Tk()  #will create tkinter object // here frame

	def leave():
		popup.destroy()

	popup.wm_title("dialog trial")
	label = ttk.Label(popup, text=msg , font= NORM_FONT)
	label.pack(side="top",fill="x",pady=10)

	B1 = ttk.Button(popup , text="okay", command = leave)
	B1.pack()


	#popup.geometry("300x150")
	popup.mainloop()

def animate(i) :



	#Interval required 5 minutes
	dataframe = yf.download(tickers=f"{stock}.ns", period=f"{DataPace}",  interval=f"{resampleSize}")

	#print(stock)

	df = dataframe.reset_index()


	df["Datetime"] = df['Datetime'].dt.tz_localize(None)

	#df["Datetime"] = np.array(df["Datetime"]).astype("datetime64[s]")
	#dftime = df["Datetime"].tolist()


	a = plt.subplot2grid((5,3),(1,0),rowspan =4, colspan=3)
	#a2 = plt.subplot2grid((6,4),(5,0),rowspan = 1 , colspan = 4 , sharex = a)
	a.clear()
	df["EMA"]=df["Close"].ewm(span=10,adjust=False).mean()

	df["SMA"]=df["Close"].rolling(20).mean()

	df["SMA"].fillna( method ='ffill', inplace = True)
	df.dropna()

	df2 = df.iloc[[-1]]


	# ohlc = df.loc[:, ['Datetime', 'Open', 'High', 'Low', 'Close']]
	# ohlc['Datetime'] = pd.to_datetime(ohlc['Datetime'])
	# ohlc['Datetime'] = ohlc['Datetime'].apply(mpl_dates.date2num)
	# ohlc = ohlc.astype(float)

	# Creating Subplots
	#fig, ax = plt.subplots()

	a.plot(df["Datetime"],df["SMA"],"#183A54",label="SMA")
	a.plot(df["Datetime"],df["EMA"],"#00A3E0",label="EMA")    #linewidth=10
	a.plot(df["Datetime"],df["Close"],"#00ff00",label="Current Prise",linewidth=3)

	# candlestick_ohlc(a, ohlc.values, width=candleWidth, colorup='green', colordown='red',  alpha = 0.8)

	a.legend(bbox_to_anchor=(0,1.02, 1 , .102), loc=3,ncol=2, borderaxespad=0)
	title = "Auto BUY/SELL by EMA-SMA\n" + str(stock) +  "\nLast Price: " + str(df2["Close"].values) + "\n" + "Time Frame: " + f"{DataPace}" + " Interval: " + f"{resampleSize}"
	a.set_title(title)




	#dataframe = yf.download(tickers=f"{stock}.ns", period=f"{DataPace}", interval=f"{resampleSize}")




	#df = dataframe.reset_index()

	#df["Datetime"] = df['Datetime'].dt.tz_localize(None)




	#dftime = df["Datetime"].tolist()


	#df["SMA"] = df["Close"].rolling(20).mean()

	#df["10dayEMA"]=df["Close"].ewm(span=10,adjust=False).mean()

	#df.fillna( method ='ffill', inplace = True)
	#df.dropna()

	from datetime import datetime

	now = datetime.now()
	#print(now)
	#start_date = "2021-06-21 11:15:00"
	after_start_date = df["Datetime"] >= now

	df = df.loc[after_start_date]


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





class tkinterApp(tk.Tk):

	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):

		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)

		tk.Tk.wm_title(self, "Trading analysis")
		# creating a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)



		menubar = tk.Menu(self, background='#ffcc99', foreground='black', activebackground='white', activeforeground='black')

		# file = tk.Menu(menubar, tearoff = 0, background='#ffcc99', foreground='black')
		# menubar.add_cascade(label ='File', menu = file)
		# file.add_command(label ='New File', command = lambda: popupmsg("Not supported yet"))
		# file.add_command(label ='Open...', command = None)
		# file.add_command(label ='Save', command = None)
		# file.add_separator()
		# file.add_command(label ='Exit', command = None)
		tk.Tk.config(self,menu = menubar)

		dataTF = tk.Menu(menubar, tearoff=1)
		#dataTF.add_command(label="1 Hour",command=lambda: changeTimeFrame('1h'))
		dataTF.add_command(label="1 Day",command=lambda: changeTimeFrame('1d'))
		dataTF.add_command(label="5 Day",command=lambda: changeTimeFrame('5d'))
		dataTF.add_command(label="1 Week",command=lambda: changeTimeFrame('7d'))
		#dataTF.add_command(label="1 Month",command=lambda: changeTimeFrame('1mo'))
		#dataTF.add_command(label="3 Month",command=lambda: changeTimeFrame('3mo'))
		menubar.add_cascade(label = "Data Time Frame", menu = dataTF)

		OHLCI = tk.Menu(menubar, tearoff=1)

		OHLCI.add_command(label = "1 minute", command = lambda: changeSampleSize('1m',0.0005))
		OHLCI.add_command(label = "5 minute", command = lambda: changeSampleSize('5m',0.003))
		OHLCI.add_command(label = "15 minute", command = lambda: changeSampleSize('15m',0.008))
		OHLCI.add_command(label = "30 minute", command = lambda: changeSampleSize('30m',0.032))
		#OHLCI.add_command(label = "1 ", command = lambda: changeSampleSize('1h',0.096))
		menubar.add_cascade(label="  Interval",menu=OHLCI)

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (StartPage, Page1, Page2, Page3, Page4, Page5):

			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")
		self.show_frame(StartPage)






	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

# first window frame startpage
class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		# label of frame Layout 2
		label = ttk.Label(self, text ="Startpage", font = LARGEFONT)

		# putting the grid in its place by using
		# grid
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		button1 = ttk.Button(self, text ="EMA & SMA",
		command = lambda : controller.show_frame(Page1))

		# putting the button in its place by
		# using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		## button to show frame 2 with text layout2
		button2 = ttk.Button(self, text ="Max Profit and Loss",
		command = lambda : controller.show_frame(Page2))

		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)

		button3 = ttk.Button(self, text ="Ratio Exit",
		command = lambda : controller.show_frame(Page3))

		button3.grid(row = 3, column = 1, padx = 10, pady = 10)

		button4 = ttk.Button(self, text ="Auto Exit",
		command = lambda : controller.show_frame(Page4))

		button4.grid(row = 4, column = 1, padx = 10, pady = 10)

		button5 = ttk.Button(self, text ="Page 5",
		command = lambda : controller.show_frame(Page5))

		button5.grid(row = 5, column = 1, padx = 10, pady = 10)




# second window frame page1
class Page1(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)


		canvas = FigureCanvasTkAgg(f, self)
		canvas.draw()

		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		button1 = ttk.Button(self, text ="Main Menu",
							command = lambda : controller.show_frame(StartPage))
		button1.pack(pady=10, padx=10,side=tk.LEFT)

		toolbar = NavigationToolbar2Tk(canvas, self)
		toolbar.update()
		toolbar.pack(side=tkinter.TOP, fill=tkinter.X)

		x1= "hallo"



		#label = tk.Label(self, text= 'Current Value: ',font=('helvetica', 12))
		#label.pack(side=tkinter.BOTTOM , pady =2 )

		#label2_title = "Invested Amount" + invested
		#label2 = tk.Label(self, text= 'Invested Amount',font=('helvetica', 12))
		#label2.pack(side=tkinter.BOTTOM , pady =2 )

		label3 = tk.Label(self, text= 'Enter Qunatity to BUY  ',font=('helvetica', 12))
		label3.pack(side=tkinter.BOTTOM , pady =2 )

		entry1 = tk.Entry (self)
		entry1.pack(side=tkinter.BOTTOM, pady=2 )


		label4 = tk.Label(self, text= 'Enter Symobol, eg. RELIANCE ',font=('helvetica', 10))
		label4.pack(side=tkinter.BOTTOM , pady =2 )

		entry2 = tk.Entry (self)
		entry2.pack(side=tkinter.BOTTOM, pady=2 )







		#x1 = 5

		def squareroot():
			global x1

			x1 = entry1.get()

			if x1 != "":
				global s
				s=int(x1)

			x2 = entry2.get()

			if x2 != "":
				global stock
				stock = x2

			self.text.insert(tk.END,waiting + " \n")
			message2 = message[:]
			for x in message2:
  				self.text.insert(tk.END,x + " \n")

			self.text.insert(tk.END,status_sell1 + " \n \n")
			self.text.insert(tk.END,"Invested Amount " + invested + " \n")
			self.text.insert(tk.END,"Profit/Loss " + profit + " \n")
			self.text.insert(tk.END, " \n \n \n \n")

			message2.clear()



			#self.text.insert(tk.END,x1 + " \n")
			#self.text.insert(tk.END,x1 + " \n")
			#print("hallo",stock)
			#self.text.delete(1.0,END)
			#self.text.delete('0.0', END)
			#self.text.delete('0.0', END)
        	#self.text.insert('0.0', "hallo")
        	#self.text.configure(state=DISABLED)

		def show():
			#self.text.insert(tk.END,status_sell + " \n")
			#self.text.insert(tk.END,status_sell1 + " \n \n")
			self.text.insert(tk.END,waiting + " \n")
			message2 = message[:]
			for x in message2:
  				self.text.insert(tk.END,x + " \n")

			self.text.insert(tk.END,status_sell1 + " \n \n")
			self.text.insert(tk.END,"Invested Amount " + invested + " \n")
			self.text.insert(tk.END,"Profit/Loss " + profit + " \n")
			self.text.insert(tk.END, " \n \n \n \n")

			message2.clear()



		button3 = ttk.Button(self, text = "Refresh BUY/SELL Status", command = show)
		button3.pack(side=tkinter.BOTTOM,pady=5, padx=5)



		button1 = ttk.Button(self, text ="PROCEED", command = squareroot)
		button1.pack(side=tkinter.BOTTOM,pady=5, padx=5)


		self.text = tkst.ScrolledText(self)
		self.text.pack()


		#self.text.delete('1.0', END)

		#txt = tk.Text(self, font=('Verdana',8))
		#txt.pack()
		#txt.insert(tk.END , "hallo")


		# Create text widget and specify size.
		#T = Text(self, height = 5, width = 52)
		#text = Text(self)

# third window frame page2
class Page2(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)



		label = ttk.Label(self, text ="max profit and loss", font = LARGEFONT)
		label.pack()

		share_symbol=tk.StringVar()	
		ttk.Label(self, text = 'Enter Symbol', font=('calibre',10, 'bold')).pack() 
		ttk.Entry(self,textvariable = share_symbol, font=('calibre',10,'normal')).pack()
	

		profit_cap=tk.StringVar()	
		ttk.Label(self, text = 'Enter ProfitCap', font=('calibre',10, 'bold')).pack()
		ttk.Entry(self,textvariable = profit_cap, font=('calibre',10,'normal')).pack()
		

		loss_cap=tk.StringVar()	
		ttk.Label(self, text = 'Enter Loss cap', font=('calibre',10, 'bold')).pack()
		ttk.Entry(self,textvariable = loss_cap, font=('calibre',10,'normal')).pack()
	

		number_of_share=tk.StringVar()	
		ttk.Label(self, text = 'Enter Number Of shares', font=('calibre',10, 'bold')).pack()
		ttk.Entry(self,textvariable = number_of_share, font=('calibre',10,'normal')).pack()

		ttk.Button(self, text ="Run Profit Loss",
							command = lambda : Thread(target = lambda :profit_loss.Max(share_symbol.get(),profit_cap.get(),loss_cap.get(),number_of_share.get()))
							.start()).pack()
		
		


		button2 = ttk.Button(self, text ="Main Menu",
							command = lambda : controller.show_frame(StartPage))
		button2.pack()



class Page3(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="ratio exit", font = LARGEFONT)
		label.pack()
      
		share_symbol=tk.StringVar()	
		ttk.Label(self, text = 'Enter Symbol', font=('calibre',10, 'bold')).pack() 
		ttk.Entry(self,textvariable = share_symbol, font=('calibre',10,'normal')).pack()


		ratio=tk.StringVar()	
		ttk.Label(self, text = 'Enter Ratio', font=('calibre',10, 'bold')).pack()
		ttk.Entry(self,textvariable = ratio, font=('calibre',10,'normal')).pack()


		risk_amount=tk.StringVar()	
		ttk.Label(self, text = 'Enter risk amount', font=('calibre',10, 'bold')).pack()
		ttk.Entry(self,textvariable = risk_amount, font=('calibre',10,'normal')).pack()


		number_of_share=tk.StringVar()	
		ttk.Label(self, text = 'Enter Number Of shares', font=('calibre',10, 'bold')).pack() 
		ttk.Entry(self,textvariable = number_of_share, font=('calibre',10,'normal')).pack()

		ttk.Button(self, text ="Run Ratio",
							command = lambda : Thread(target = lambda :ratio_exit.ratio(share_symbol.get(),number_of_share.get(),ratio.get(),risk_amount.get(),))
							.start()).pack()



		button2 = ttk.Button(self, text ="Main Menu",
							command = lambda : controller.show_frame(StartPage))
		button2.pack()

class Page4(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		#symbol
		share_symbol=tk.StringVar()	
		ttk.Label(self, text = 'Enter Symbol', font=('calibre',10, 'bold')).grid(row=0, column=0, padx=10, pady=2.5)
		ttk.Entry(self,textvariable = share_symbol, font=('calibre',10,'normal')).grid(row=0, column=1, padx=10, pady=2.5)

		#number of share
		number_of_share=tk.StringVar()	
		ttk.Label(self, text = 'Enter Number Of shares', font=('calibre',10, 'bold')).grid(row=2, column=0, padx=10, pady=2.5)
		ttk.Entry(self,textvariable = number_of_share, font=('calibre',10,'normal')).grid(row=2, column=1, padx=10, pady=2.5)

		# starttime
		ttk.Label(self, text="Enter Starting Time:").grid(row=3, column=0, padx=10, pady=2.5)

		ttk.Label(self, text="Hour:").grid(row=3, column=1, padx=10, pady=2.5)
		shour = tk.StringVar(value="Select an Hour")
		options = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13",
						"14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "00"]
		h = ttk.OptionMenu(self, shour, *options)
		h.grid(row=3, column=2, padx=10, pady=2.5)

		ttk.Label(self, text="Minute:").grid(row=4, column=1, padx=10, pady=2.5)
		sminute = tk.StringVar(value="Select an Minute")
		options = ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"]
		h = ttk.OptionMenu(self, sminute, *options)
		h.grid(row=4, column=2, padx=10, pady=2.5)

		# endingtime
		ttk.Label(self, text="Enter Ending Time:").grid(row=5, column=0, padx=10, pady=2.5)

		ttk.Label(self, text="Hour:").grid(row=5, column=1, padx=10, pady=2.5)
		ehour = tk.StringVar(value="Select an Hour")
		options = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13",
						"14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "00"]
		h = ttk.OptionMenu(self, ehour, *options)
		h.grid(row=5, column=2, padx=10, pady=2.5)

		ttk.Label(self, text="Minute:").grid(row=6, column=1, padx=10, pady=2.5)
		eminute = tk.StringVar(value="Select an Minute")
		options = ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"]
		h = ttk.OptionMenu(self, eminute, *options)
		h.grid(row=6, column=2, padx=10, pady=2.5)

		ttk.Button(self, text="Next",
					command=lambda: time_dependend.run_auto_exit(share_symbol.get(), number_of_share.get(),shour.get(), sminute.get(),ehour.get(),eminute.get())).grid(row=10, column=10, padx=5, pady=5)
      
      
		button2 = ttk.Button(self, text ="Main Menu",
							command = lambda : controller.show_frame(StartPage))
		button2.grid(row=10, column=0, padx=5, pady=5)

class Page5(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label = ttk.Label(self, text ="Page 5", font = LARGEFONT)
		label.pack()

		button2 = ttk.Button(self, text ="Main Menu",
							command = lambda : controller.show_frame(StartPage))
		button2.pack()


# Driver Code
app = tkinterApp()
app.geometry("1080x800")
ani = animation.FuncAnimation(f,animate,interval=3000)  #plot will update after 3s
app.mainloop()
