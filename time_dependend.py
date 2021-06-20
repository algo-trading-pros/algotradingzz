from numpy import true_divide
from yahoo_fin import stock_info as si
from datetime import datetime
import time
import csv_fileHandler
import tkinter as tk 
from threading import Thread
from time import sleep

def run_auto_exit(share_symbol:str,shares_number,startHour,startMin,endHour,endMin):
   shares_number=float(shares_number)

   starting_price= si.get_live_price(f"{share_symbol.upper()}.ns")
   amount_invested=shares_number*starting_price
   
   window = tk.Tk()

   label = tk.Label(window,text=f"Starting price: {starting_price}",font=('calibre',10, 'bold'))
   label.pack()

   label = tk.Label(window,text=f"Amount Invested: {amount_invested}",font=('calibre',10, 'bold'))
   label.pack()

   waiting=tk.Label(window,text="Waiting for Starting time...",font=('calibre',10, 'bold'))
   waiting.pack()
   
   def check():
            while True:
                  sleep(1)
                  if time.strftime('%H')==startHour and time.strftime('%M')==startMin:
                     waiting.config(text="Waiting for end time...")
                     waiting.update()
                     while True:
                        sleep(1)
                        if time.strftime('%H')==endHour and time.strftime('%M')==endMin:
                           break
                     break
                        

            ending_price= si.get_live_price(f"{share_symbol}.ns")
            diffrence=ending_price*shares_number-amount_invested
            if diffrence>=0:
               exitPrice=tk.Label(window,text=f"Exit price :{ending_price}",font=('calibre',10, 'bold'))
               exitPrice.pack()
               exitPrice=tk.Label(window,text=f"Profit of : {diffrence}",font=('calibre',10, 'bold'))
               exitPrice.pack()
            else:
               exitPrice=tk.Label(window,text=f"Exit price :{ending_price}",font=('calibre',10, 'bold'))
               exitPrice.pack()
               exitPrice=tk.Label(window,text=f"Loss of :{diffrence}",font=('calibre',10, 'bold'))
               exitPrice.pack()
   
   Thread(target= check).start()
   

   window.mainloop()


def draw_window():

   def quitAndRun(root):
      root.destroy()
      run_auto_exit( share_symbol.get(), number_of_share.get(),shour.get(), sminute.get(),ehour.get(),eminute.get()
                                                )


   root = tk.Tk()
   root.title("Automated exit")

   #symbol
   share_symbol=tk.StringVar()	
   tk.Label(root, text = 'Enter Symbol', font=('calibre',10, 'bold')).grid(row=0, column=0, padx=10, pady=2.5)
   tk.Entry(root,textvariable = share_symbol, font=('calibre',10,'normal')).grid(row=0, column=1, padx=10, pady=2.5)

   #number of share
   number_of_share=tk.StringVar()	
   tk.Label(root, text = 'Enter Number Of shares', font=('calibre',10, 'bold')).grid(row=2, column=0, padx=10, pady=2.5)
   tk.Entry(root,textvariable = number_of_share, font=('calibre',10,'normal')).grid(row=2, column=1, padx=10, pady=2.5)

   # starttime
   tk.Label(root, text="Enter Starting Time:").grid(row=3, column=0, padx=10, pady=2.5)

   tk.Label(root, text="Hour:").grid(row=3, column=1, padx=10, pady=2.5)
   shour = tk.StringVar(value="Select an Hour")
   options = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13",
               "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "00"]
   h = tk.OptionMenu(root, shour, *options)
   h.grid(row=3, column=2, padx=10, pady=2.5)

   tk.Label(root, text="Minute:").grid(row=4, column=1, padx=10, pady=2.5)
   sminute = tk.StringVar(value="Select an Minute")
   options = ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"]
   h = tk.OptionMenu(root, sminute, *options)
   h.grid(row=4, column=2, padx=10, pady=2.5)

   # endingtime
   tk.Label(root, text="Enter Ending Time:").grid(row=5, column=0, padx=10, pady=2.5)

   tk.Label(root, text="Hour:").grid(row=5, column=1, padx=10, pady=2.5)
   ehour = tk.StringVar(value="Select an Hour")
   options = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13",
               "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "00"]
   h = tk.OptionMenu(root, ehour, *options)
   h.grid(row=5, column=2, padx=10, pady=2.5)

   tk.Label(root, text="Minute:").grid(row=6, column=1, padx=10, pady=2.5)
   eminute = tk.StringVar(value="Select an Minute")
   options = ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"]
   h = tk.OptionMenu(root, eminute, *options)
   h.grid(row=6, column=2, padx=10, pady=2.5)

   tk.Button(root, text="Next", padx=15, pady=2.5, fg="black", bg="white",
            command=lambda: quitAndRun(root)).grid(row=10, column=10, padx=5, pady=5)
   root.mainloop()


draw_window()