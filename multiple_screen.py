import tkinter as tk
from tkinter import ttk
#import matplotlib
#matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.animation as animation
from matplotlib import style
import pandas as pd
from yahoo_fin import stock_info as si
import numpy as np



LARGEFONT =("Verdana", 35)
style.use("ggplot")

f = Figure(figsize=(10,6),dpi=100)
a = f.add_subplot(111)
"""
def animate(i) :
	pullData = open("dataset","r").read()
	dataList = pullData.split('\n')
	xList = []
	yList = []
	for eachLine in dataList:
		if len(eachLine) > 1:
			x, y =eachLine.split(',')
			xList.append(int(x))
			yList.append(int(y))
	a.clear()
	a.plot(xList,yList)
"""
def animate(i) :
	reliance_data=si.get_data("RELIANCE.ns")

	dataframe=pd.DataFrame(reliance_data)


	dataframe["EMA"]=dataframe["close"].ewm(span=10,adjust=False).mean()

	dataframe["SMA"]=dataframe["close"].rolling(20).mean()

	dataframe["SMA"].fillna( method ='ffill', inplace = True)

	df1 = dataframe.reset_index()
	df = df1.rename(columns = {'index': 'Date'}, inplace = False)
	df2 = df.iloc[[-1]]
	a.clear()

	a.plot(df["Date"],df["EMA"],"#00A3E0",label="10dayEMA")
	a.plot(df["Date"],df["SMA"],"#183A54",label="SMA")
	a.legend(bbox_to_anchor=(0,1.02, 1 , .102), loc=3,ncol=2, borderaxespad=0)
	title = "EMA & SMA comparison\nLast Price: " + str(df2["close"].values)
	a.set_title(title)




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
		button2 = ttk.Button(self, text ="Page 2",
		command = lambda : controller.show_frame(Page2))

		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)

		button3 = ttk.Button(self, text ="Page 3",
		command = lambda : controller.show_frame(Page3))

		button3.grid(row = 3, column = 1, padx = 10, pady = 10)

		button4 = ttk.Button(self, text ="Page 4",
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


		toolbar = NavigationToolbar2Tk(canvas, self)
		toolbar.update()

		button1 = ttk.Button(self, text ="Main Menu",
							command = lambda : controller.show_frame(StartPage))
		button1.pack(pady=10, padx=10)

		# Create text widget and specify size.
		#T = Text(self, height = 5, width = 52)
		#text = Text(self)



# third window frame page2
class Page2(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Page 2", font = LARGEFONT)
		label.pack()

		button2 = ttk.Button(self, text ="Main Menu",
							command = lambda : controller.show_frame(StartPage))
		button2.pack()

class Page3(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Page 3", font = LARGEFONT)
		label.pack()

		button2 = ttk.Button(self, text ="Main Menu",
							command = lambda : controller.show_frame(StartPage))
		button2.pack()

class Page4(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Page 4", font = LARGEFONT)
		label.pack()

		button2 = ttk.Button(self, text ="Main Menu",
							command = lambda : controller.show_frame(StartPage))
		button2.pack()

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
ani = animation.FuncAnimation(f,animate,interval=300000)  #plot will update after 300s
app.mainloop()
