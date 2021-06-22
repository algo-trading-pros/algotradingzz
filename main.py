import tkinter
import tkinter as tk
from tkinter import Frame, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.animation as animation
from matplotlib import style
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
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.dates as mpl_dates
import yfinance as yf
import tkinter.scrolledtext as tkst
import time
import store_state
from EMA_SMA import *
from datetime import datetime
from tkinter import *

LARGEFONT =("Verdana", 35)
style.use("ggplot")
LARGEFONT =("Verdana", 35)
NORM_FONT =("Verdana", 15)
SMLL_FONT =("Verdana", 10)


#a = f.add_subplot(111)
#
# stock = "RELIANCE"
# DatCounter =9000
#
# resampleSize = "5m"
# DataPace = "1d"
# candleWidth = 0.008
# s=0

def makeAThread(function):
    Thread(target = function).start()






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

		label =ttk.Label(self, text ="EMA-SMA Auto buy",  font=('calibre',15, 'bold'))
		label.grid(row=0 , column = 1 , columnspan = 2,rowspan=1)

		labelt =ttk.Label(self, text ="TimeFrame :",  font=('calibre',10, 'bold'))
		labelt.grid(row=1 , column = 0 , sticky = E)

		labelf =ttk.Label(self, text ="Interval :",  font=('calibre',10, 'bold'))
		labelf.grid(row=1 , column = 2 ,sticky = E)

		labelg =ttk.Label(self, text ="",  font=('calibre',10, 'bold'))
		labelg.grid(row=2 , column = 0 , columnspan = 2)

		labelh =ttk.Label(self, text ="",  font=('calibre',10, 'bold'))
		labelh.grid(row=2 , column = 2 ,columnspan = 2)

		symbol=tk.StringVar()
		ttk.Label(self, text = 'Enter Symbol', font=('calibre',10, 'bold')).grid(row = 3, column = 0, sticky = W, pady = 2)
		ttk.Entry(self, textvariable = symbol).grid(row = 3, column = 1, pady = 2)


		quantity=tk.StringVar()
		ttk.Label(self, text = 'Qunatity to Buy/Sell', font=('calibre',10, 'bold')).grid(row = 4, column = 0, sticky = W, pady = 2)
		ttk.Entry(self,textvariable = quantity).grid(row = 4, column = 1, pady = 2)



		ttk.Label(self, text = ' ', font=('calibre',10, 'bold')).grid(row = 5, column = 0, sticky = W ,pady = 2)
		ttk.Label(self, text = ' ', font=('calibre',10, 'bold')).grid(row = 5, column = 1, sticky = W ,pady = 2)


		ttk.Label(self, text = 'Invested value:', font=('calibre',10, 'bold')).grid(row = 7, column = 0, sticky = W ,pady = 2)

		ttk.Label(self, text = 'Current value / share:', font=('calibre',10, 'bold')).grid(row = 8, column = 0 , sticky =W, pady =2)

		ttk.Label(self, text = 'Profit/Loss', font=('calibre',10, 'bold')).grid(row = 9, column = 0, sticky = W, pady = 2)


		T3 = Text(self , height = 1 , width = 18)
		T3.grid(row=7,column=1, sticky=E, padx= 5 , pady = 5)

		T4=  Text(self, height = 1,width = 18 )
		T4.grid(row=8,column=1, sticky=E, padx= 5 , pady = 5)
		#
		T5=  Text(self, height = 1,width = 18 )
		T5.grid(row=9,column=1, sticky=E, padx= 5 , pady = 5)

		#
		T = Text(self, height = 5 )
		T.grid(row=3,column=2,columnspan = 2 , rowspan= 3 , sticky=E, padx= 5 , pady = 5)



		def proceed():

			# from datetime import datetime
			global now
			global x1
			global s
			DataPace = ehhour.get()

			resampleSize = interval.get()
			now = datetime.now()
			quantity1 = int(quantity.get())
			symbol1 = symbol.get()
			# print("========",quantity1,symbol1)

			T.delete("1.0","end")
			T3.delete("1.0","end")
			T4.delete("1.0","end")
			T5.delete("1.0","end")


			x1 = quantity1
			if x1 != "":

				# s=int(x1)
				s = x1
				# print(type(x1))
			x2 = symbol1
			if x2 != "":
				global stock
				stock = x2
			# print("********",stock,s)

			list = EMA_SMA(stock,s,now,resampleSize,DataPace)
			last_price = list[0]
			status_sell1 = list[1]
			message = list[2]
			invested = list[3]
			profit = list[4]
			waiting = list[5]


			T.insert(tk.END, waiting + "\n")
			message2 = message[:]
			T.insert(tk.END,"STOCK : " + stock +" \n")
			for x in message2:
				T.insert(tk.END,x + " \n")
			# T.insert(tk.END,"\n")
			T.insert(tk.END,"Invested Amount " + invested + " \n")
			T.insert(tk.END,"Profit/Loss " + profit + " \n")
			T.insert(tk.END, " \n")
			T3.insert(tk.END,invested)
			T4.insert(tk.END,last_price)
			T5.insert(tk.END,profit)

			message2.clear()


		def show():
			# symbol = entry2.get()
			# quantity = entry1.get()
			DataPace = ehhour.get()

			resampleSize = interval.get()
			# print("******" , DataPace ,resampleSize)
			# EMA_SMA(stock,s,now,resampleSize,DataPace)
			list = EMA_SMA(stock,s,now,resampleSize,DataPace)
			last_price = list[0]
			status_sell1 = list[1]
			message = list[2]
			invested = list[3]
			profit = list[4]
			waiting = list[5]

			T.delete("1.0","end")
			T3.delete("1.0","end")
			T4.delete("1.0","end")
			T5.delete("1.0","end")
			# self.text.insert(tk.END,waiting + " \n")
			T.insert(tk.END,waiting + " \n")

			T.insert(tk.END,"STOCK: " + stock +" \n")
			message2 = message[:]
			for x in message2:
  				# self.text.insert(tk.END,x + " \n")
				T.insert(tk.END,x + " \n")

			T.insert(tk.END,"\n")
			T.insert(tk.END,"Invested Amount " + invested + " \n")
			T.insert(tk.END,"Profit/Loss " + profit + " \n")
			T3.insert(tk.END,invested)
			T4.insert(tk.END,last_price)
			T5.insert(tk.END,profit)




			message2.clear()




		button2 = ttk.Button(self, text ="PROCEED", command = proceed)
		button2.grid(row = 6, column = 1, sticky = W ,pady = 2)


		button3 = ttk.Button(self, text ="REFRESH", command = show)
		button3.grid(row = 6, column = 2, sticky = E ,pady = 2)






		button1 = ttk.Button(self, text ="Main Menu", command = lambda : controller.show_frame(StartPage))
		button1.grid(row = 10, column = 1, sticky = W ,pady = 7)


		ehhour = tk.StringVar()
		options = ["1d","1d", "5d", "7d"]
		timef = ttk.OptionMenu(self, ehhour, *options)
		timef.grid(row=1, column=1, padx=10, pady=1 , sticky = W)

		interval = tk.StringVar()
		options = ["5m","1m", "5m", "15m" , "30m"]
		inters = ttk.OptionMenu(self, interval, *options)
		inters.grid(row=1, column=3, padx=10, pady=1 , sticky = W)



# third window frame page2
class Page2(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		data=store_state.readConfig("profit_loss")

		label = ttk.Label(self, text ="max profit and loss", font = LARGEFONT)
		label.pack()

		share_symbol=tk.StringVar(self,data[0])	
		ttk.Label(self, text = 'Enter Symbol', font=('calibre',10, 'bold')).pack() 
		ttk.Entry(self,textvariable = share_symbol, font=('calibre',10,'normal')).pack()
	

		profit_cap=tk.StringVar(self,data[1])	
		ttk.Label(self, text = 'Enter ProfitCap', font=('calibre',10, 'bold')).pack()
		ttk.Entry(self,textvariable = profit_cap, font=('calibre',10,'normal')).pack()
		

		loss_cap=tk.StringVar(self,data[2])	
		ttk.Label(self, text = 'Enter Loss cap', font=('calibre',10, 'bold')).pack()
		ttk.Entry(self,textvariable = loss_cap, font=('calibre',10,'normal')).pack()
	

		number_of_share=tk.StringVar(self,data[3])	
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

		data=store_state.readConfig("ratio_exit")
      
		share_symbol=tk.StringVar(self,data[0])	
		ttk.Label(self, text = 'Enter Symbol', font=('calibre',10, 'bold')).pack() 
		ttk.Entry(self,textvariable = share_symbol, font=('calibre',10,'normal')).pack()


		ratio=tk.StringVar(self,data[1])	
		ttk.Label(self, text = 'Enter Ratio', font=('calibre',10, 'bold')).pack()
		ttk.Entry(self,textvariable = ratio, font=('calibre',10,'normal')).pack()


		risk_amount=tk.StringVar(self,data[2])	
		ttk.Label(self, text = 'Enter risk amount', font=('calibre',10, 'bold')).pack()
		ttk.Entry(self,textvariable = risk_amount, font=('calibre',10,'normal')).pack()


		number_of_share=tk.StringVar(self,data[3])	
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
		

		data=store_state.readConfig("time_dependend")
		#symbol
		share_symbol=tk.StringVar(self,data[0])	
		ttk.Label(self, text = 'Enter Symbol', font=('calibre',10, 'bold')).grid(row=0, column=0, padx=10, pady=2.5)
		ttk.Entry(self,textvariable = share_symbol, font=('calibre',10,'normal')).grid(row=0, column=1, padx=10, pady=2.5)

		#number of share
		number_of_share=tk.StringVar(self,data[1])	
		ttk.Label(self, text = 'Enter Number Of shares', font=('calibre',10, 'bold')).grid(row=2, column=0, padx=10, pady=2.5)
		ttk.Entry(self,textvariable = number_of_share, font=('calibre',10,'normal')).grid(row=2, column=1, padx=10, pady=2.5)

		# starttime
		ttk.Label(self, text="Enter Starting Time:").grid(row=3, column=0, padx=10, pady=2.5)

		ttk.Label(self, text="Hour:").grid(row=3, column=1, padx=10, pady=2.5)
		shour = tk.StringVar(value=data[2])
		options = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13",
						"14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "00"]
		h = ttk.OptionMenu(self, shour, *options)
		h.grid(row=3, column=2, padx=10, pady=2.5)

		ttk.Label(self, text="Minute:").grid(row=4, column=1, padx=10, pady=2.5)
		sminute = tk.StringVar(value=data[3])
		options = ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"]
		h = ttk.OptionMenu(self, sminute, *options)
		h.grid(row=4, column=2, padx=10, pady=2.5)

		# endingtime
		ttk.Label(self, text="Enter Ending Time:").grid(row=5, column=0, padx=10, pady=2.5)

		ttk.Label(self, text="Hour:").grid(row=5, column=1, padx=10, pady=2.5)
		ehour = tk.StringVar(value=data[4])
		options = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13",
						"14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "00"]
		h = ttk.OptionMenu(self, ehour, *options)
		h.grid(row=5, column=2, padx=10, pady=2.5)

		ttk.Label(self, text="Minute:").grid(row=6, column=1, padx=10, pady=2.5)
		eminute = tk.StringVar(value=data[5])
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
app.geometry("1080x720")
# f = plt.figure()
# ani = animation.FuncAnimation(f,animate,interval=3000)  #plot will update after 3s
app.mainloop()
