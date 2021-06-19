from yahoo_fin import stock_info as si
from time import sleep
import tkinter as tk
from threading import Thread

def Max(share_symbol:str,profit_cap,loss_cap,number_of_share):

        ##taking inputs
        share_symbol=share_symbol.upper()
        profit_cap=int(profit_cap)
        loss_cap=int(loss_cap)
        number_of_share=int(number_of_share)

        change_in_stock_price_for_profit=profit_cap/number_of_share
        change_in_stock_price_for_loss=loss_cap/number_of_share

        containers1=si.get_live_price(f"{share_symbol}.ns")
        current_price = containers1
        target_price_profit=current_price+change_in_stock_price_for_profit
        target_price_loss=current_price-change_in_stock_price_for_loss
        amount_invested=number_of_share*current_price

        ##tkinter window

        window = tk.Tk()

        label = tk.Label(window,text=f"current price: {current_price},Amount Invested: {amount_invested}",font=('calibre',10, 'bold'))
        label.pack()
  
        proft=tk.Label(window,text="Checking for profits..",font=('calibre',10, 'bold'))
        proft.pack()
        loss=tk.Label(window,text="Checking for loss..",font=('calibre',10, 'bold'))
        loss.pack()
        def check():
                while True:
                        sleep(1)
                        containers1=si.get_live_price(f"{share_symbol}.ns")
                        current_price_new=containers1

                        if current_price_new>target_price_profit:
                                profit_made=(current_price_new-current_price)*number_of_share
                                proft.config(text=f"You made a profit of {profit_made}. Not checking anymore").update()
                                break
                        if current_price_new<target_price_loss:
                                loss_made = (current_price_new - current_price) * number_of_share
                                loss.config(text=f"you made a loss of {loss_made}. Not checking anymore").update()
                                break
        
        Thread(target=check).start()
        

        window.mainloop()


        

        

        