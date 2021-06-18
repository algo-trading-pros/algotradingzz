from yahoo_fin import stock_info as si

def Max():
        share_purchased=input("Enter the symbol of share you want to purchase").upper()
        profit_cap=int(input("What is maximum profit do you want to set: "))
        loss_cap=int(input("What is maximum Loss do you want to set: "))
        number_of_share=int(input("how many shares you would love to buy: "))
        change_in_stock_price_for_profit=profit_cap/number_of_share
        change_in_stock_price_for_loss=loss_cap/number_of_share

        containers1=si.get_live_price(f"{share_purchased}.ns")
        current_price = containers1
        target_price_profit=current_price+change_in_stock_price_for_profit
        target_price_loss=current_price-change_in_stock_price_for_loss
        amount_invested=number_of_share*current_price
        print(f"current price: {current_price},Amount Invested: {amount_invested}")
        while True:

                containers1=si.get_live_price(f"{share_purchased}.ns")
                current_price_new=containers1

                if current_price_new>target_price_profit:
                        print(current_price_new)
                        profit_made=(current_price_new-current_price)*number_of_share
                        print(f"You made a profit of {profit_made}")
                        break
                if current_price_new<target_price_loss:
                        loss_made = (current_price_new - current_price) * number_of_share
                        print(current_price_new)
                        print(f"you made a loss of {loss_made}")
                        break

Max()