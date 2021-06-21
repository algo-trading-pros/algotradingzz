
from yahoo_fin import stock_info as si
import tkinter as tk
from threading import Thread
import store_state

def ratio(share_symbol:str,number_of_share,ratio_rnr,risk_amount):

    share_sybol=share_symbol.upper()
    number_of_share=int(number_of_share)
    ratio_rnr=float(ratio_rnr)
    risk_amount=float(risk_amount)

    store_state.saveConfig("ratio_exit",[share_symbol,ratio_rnr,risk_amount,number_of_share])

    current_price=si.get_live_price(f"{share_sybol}.ns")
    amount_invested=number_of_share*current_price
    

    stoploss_endpoint=current_price-risk_amount
    profit_target=current_price+risk_amount*((ratio_rnr)**-1)
    
    
        
    window = tk.Tk()

    label = tk.Label(window,text=f"amount invested: {amount_invested},profit target: {profit_target},current price: {current_price},stoploss endpoint: {stoploss_endpoint},",font=('calibre',10, 'bold'))
    label.pack()
    

    proft=tk.Label(window,text="Checking for profit target..",font=('calibre',10, 'bold'))
    proft.pack()
    loss=tk.Label(window,text="Checking for loss target..",font=('calibre',10, 'bold'))
    loss.pack()
    
    def check():
            while True:
                current_price_new = si.get_live_price(f"{share_sybol}.ns")
                if current_price_new  >= profit_target:
                    proft.config(text=f"Profit target hit. Profit made:  {(current_price_new-current_price)*number_of_share}").update()
                    break
                if current_price_new <= stoploss_endpoint:
                    loss.config(text=f"Loss target  hit. Loss happened :  {(-current_price_new+current_price)*number_of_share}").update()
                    break
    
    Thread(target=check).start()
    

    window.mainloop()
