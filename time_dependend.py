from numpy import true_divide
from yahoo_fin import stock_info as si
from datetime import datetime
import time
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
               waiting.config(text=f"Exit price :{ending_price}")
               waiting.update()
               exitPrice=tk.Label(window,text=f"Profit of : {diffrence}",font=('calibre',10, 'bold'))
               exitPrice.pack()
            else:
               waiting.config(text=f"Exit price :{ending_price}")
               waiting.update()
               exitPrice=tk.Label(window,text=f"Loss of :{diffrence}",font=('calibre',10, 'bold'))
               exitPrice.pack()
   
   Thread(target= check).start()
   

   window.mainloop()

