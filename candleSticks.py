from bs4 import BeautifulSoup as Soup
from yahoo_fin import stock_info as si
from datetime import datetime
import time
import csv_fileHandler


def make_candleSticks(share_symbol,candelstick_length):
    while True:
        t_end = time.time() + candelstick_length * 60
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        candlestick = {}
        current_price = 0
        MaxPrice = 0

        #making a candlestick
    
        containers1 = si.get_live_price(f"{share_symbol}.ns")
        open=containers1
        MinPrice=open
        candlestick["open"]=containers1
        candlestick["Time of opening"]=current_time
        while time.time()<t_end:
                    
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
    share_symbol=input("Share_symbol: ").capitalize()
    candelstick_length=float(input("Candle Stick Length in minutes: "))
    make_candleSticks(share_symbol,candelstick_length)

main()