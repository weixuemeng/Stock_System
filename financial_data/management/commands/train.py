from django.core.management.base import BaseCommand
from financial_data.models import Stock  
from sklearn.linear_model import LinearRegression
import numpy as np
import pickle

class Command(BaseCommand):
    help = 'Train and save the linear regression model'

    def handle(self, *args, **kwargs):
        # Fetch historical stock data
        stocks = Stock.objects.order_by('time_stamp').values_list('time_stamp', 'close_price')
        X = np.array([i for i in range(len(stocks))]).reshape(-1, 1)  
        y = np.array([stock[1] for stock in stocks])  # Closing prices

        model = LinearRegression()
        model.fit(X, y)

        # Save the trained model into a .pkl file
        with open('linear_regression_model.pkl', 'wb') as f:
            pickle.dump(model, f)

        self.stdout.write(self.style.SUCCESS('Model trained and saved successfully!'))
