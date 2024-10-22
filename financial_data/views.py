import decimal
import pickle
from django.shortcuts import render
from django.conf import settings
from .models import Stock, UserRule, StockPrediction
import requests
from django.http import JsonResponse
import numpy as np

from datetime import datetime, timedelta


# Create your views here.
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
r = requests.get(url)
data = r.json()
API_KEY = "demo"
BASE_URL = "https://www.alphavantage.co/query"

def fetch_data(stock_symbol = "IBM"):
    # get from TIME_SERIES_DAILY API 
    url = f"{BASE_URL}?function=TIME_SERIES_DAILY&symbol={stock_symbol}&outputsize=full&apikey={API_KEY}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            stock_price_data = response.json()
            time_series= stock_price_data.get("Time Series (Daily)")
            end_date= datetime.now().date()  
            start_date= end_date-timedelta(days=365 * 2)  
            for date_time, price_data in time_series.items(): # 2024-10-18 
                stock_date = datetime.strptime(date_time, "%Y-%m-%d").date() # convert date string to datetime object 
                if start_date <= stock_date <= end_date: 
                    try:
                        Stock.objects.create(
                            stock_symbol="IBM",
                            time_stamp=stock_date,
                            open_price=price_data.get("1. open"),
                            high_price=price_data.get("2. high"),
                            low_price=price_data.get("3. low"),
                            close_price=price_data.get("4. close"),
                            volume=price_data.get("5. volume"),
                        )
                        print("Successfully added to db")
                    except Exception as e:
                        print(f"Error adding to db: {e}")
                    print("add to db")
                else:
                    print("Date not in range") 
        else: # error fetching data
            return "Error fetching data {}".format(response.status_code)
    
    except Exception as e:
        return "An error occurred: {}".format(e)

def list_stock_data(request):
    fetch_data()
    stock_data = Stock.objects.all()
    return render(request, 'stock_data.html', {'stock_data': stock_data})

def backtest(request):
    if request.method =='POST':
        initial_investment = int(request.POST.get('initial_investment'))
        buy_avg_days = int(request.POST.get('buy_avg'))
        sell_avg_days = int(request.POST.get('sell_avg'))

        # create a user rule based on the input 
        rule = UserRule.objects.create(
            initial_investment=initial_investment,
            buy_avg=buy_avg_days,
            sell_avg=sell_avg_days
        )
        

        stocks = Stock.objects.filter(time_stamp__lte=datetime.now().date())
        date_prices = [[s.time_stamp, s.close_price] for s in stocks] # (date, close_price)
        drawdown = 0
        number_trades = 0
        shares=  0
        current_money = 0
        buy_share = [] # store the share we buy 
        sell_share = [] # store the share we sell 

        for i in range(len(date_prices)):
            if i>=buy_avg_days: # i= 50 
                # compute the avg
                buy_avg = sum([p[1] for p in date_prices[i-buy_avg_days: i]])/buy_avg_days # [0:50] total 50 days 

            
                # price dips below the moving average
                if date_prices[i][1] < buy_avg and shares == 0:
                    shares = initial_investment / date_prices[i][1] # Buy all
                    current_money = 0 
                    buy_share.append(date_prices[i][1])
                    number_trades += 1
                
            if i >= sell_avg_days:  
                sell_avg = sum(p[1] for p in date_prices[i-sell_avg_days:i]) / sell_avg_days
                
                # price goes above the moving average
                if date_prices[i][1] > sell_avg and shares > 0:
                    # Sell 
                    current_money += shares * date_prices[i][1] # Sell all 
                    shares = 0 
                    sell_share.append(date_prices[i][1])
                    number_trades += 1

        total_value = current_money + (shares * date_prices[-1][1])  
        total_return = total_value - initial_investment  

        peak = float('-inf')
        max_drawdown = float('-inf')

        all_prices = buy_share + sell_share
        all_prices.sort()  # Sort by price or date if needed

        for price in all_prices:
            peak = max(peak, price)
            drawdown = peak - price 
            max_drawdown = max(max_drawdown, drawdown)            

        # get the report based on user rules 
        summary = {'total_return':total_return,'max_drawdown':max_drawdown, 'number_trades':number_trades}
        
        return render(request, 'summary.html', {'results': summary})
    else:
        return render(request, 'user_rule.html')

def predictStock(request):
    if request.method == "GET": 

        with open('linear_regression_model.pkl', 'rb') as f:
            model = pickle.load(f) # load model 

        stock_number = Stock.objects.count() 
        future_days = np.array([[stock_number + i] for i in range(1, 31)])
        predictions = model.predict(future_days)
        predicted_val = []

        for i, price in enumerate(predictions):
            print(i,price)
            try:
                StockPrediction.objects.create(date=f"2024-{i+1:02d}-01", predicted_price=price) 
            except Exception as e:
                print("Error when storing predictions:", e)
            predicted_val.append((f"2024-{i+1:02d}-01",price))
        return render(request, 'predictions.html', {'predicted_stock_prices': predicted_val})
    return render(request, 'predictions.html', {})


        






    



    