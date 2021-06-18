from datetime import datetime
import csv
import csv_fileHandler
from csv import DictWriter
from yahoo_fin import stock_info as si
import os


def PortFolio():
    fieldnames_portfolio=["share_purchased","Quantity_Bought","date","Time","Bought_price","Amount_invested"]
    now = datetime.now()
    my_portfolio={}
    current_time = now.strftime("%H:%M:%S")
    current_date=f"{now.year}:{now.month}:{now.day}"
    share_purchased=input("Enter the symbol of share you want to purchase").upper()
    quantity_of_share=int(input("Enter the quantity you want to buy"))
    my_portfolio["share_purchased"]=share_purchased
    my_portfolio["Quantity_Bought"]=quantity_of_share
    my_portfolio["date"]=current_date
    my_portfolio["Time"]=current_time
    my_portfolio["Bought_price"]=round(si.get_live_price(f"{share_purchased}.ns"),2)
    my_portfolio["Amount_invested"]=quantity_of_share*round(si.get_live_price(f"{share_purchased}.ns"),2)
    my_portfolio_list=[(k,v) for k,v in my_portfolio.items() ]

    #write to csv file
    csv_fileHandler.File('Portfolio_data.csv',fieldnames_portfolio).addRow(my_portfolio)
    print(my_portfolio)

PortFolio()