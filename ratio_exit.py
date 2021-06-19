from yahoo_fin import stock_info as si
share_purchased=input("Enter the symbol of share you want to purchase").upper()
number_of_share=int(input("how many shares you would love to buy: "))
ratio_rnr=float(input("Risk / Reward Ratio"))
risk_amount=float(input("How much amount of risk dom you want to take per share"))
current_price=si.get_live_price(f"{share_purchased}.ns")
amount_invested=number_of_share*current_price
print(amount_invested)

stoploss_endpoint=current_price-risk_amount
profit_target=current_price+risk_amount*((ratio_rnr)**-1)
print(profit_target)
print(current_price)
print(stoploss_endpoint)
while True:
    current_price_new = si.get_live_price(f"{share_purchased}.ns")
    if current_price_new  >= profit_target:

        print("Profit target hit")
        print(f"Profit made:  {(current_price_new-current_price)*number_of_share}")
    if current_price_new <= stoploss_endpoint:
        print("Loss target  hit")
        print(f"Loss happened :  {(-current_price_new+current_price)*number_of_share}")
