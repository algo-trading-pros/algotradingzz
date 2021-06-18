from bs4 import BeautifulSoup as Soup
import os
from yahoo_fin import stock_info as si
import requests
from datetime import datetime
import time
import csv_fileHandler



def make_candleSticks(share_symbol):
    while True:
        t_end = time.time() + 55 * 1
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        candlestick = {}
        current_price = 0
        MaxPrice = 0

        #making a candlestick

        while time.time()<t_end:
            time.sleep(2.5)
            containers1 = si.get_live_price(f"{share_symbol}.ns")
            open=containers1
            MinPrice=open
            candlestick["open"]=containers1
            candlestick["Time of opening"]=current_time
            while time.time()<t_end:
                time.sleep(2.5)         
                containers1 = si.get_live_price(f"{share_symbol}.ns")
                current_price=containers1
                if current_price>open:
                    MaxPrice=current_price
                else: MaxPrice=open
                if current_price<open:
                    MinPrice=current_price
                candlestick["HIGH"]=MaxPrice
                candlestick["LOW"]=MinPrice
            close=current_price
            candlestick["close"]=close
        
        #writing candle stick to csv file

        csv_fileHandler.File("sample.csv",["open","Time of opening","HIGH","LOW","close"]).addRow(candlestick)
        print(candlestick)

def main():
    share_symbol=input("Share_symbol :").capitalize()
    make_candleSticks(share_symbol)

main()