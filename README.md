# Stock_System
This project is a Django-based financial stock system that fetches stock data, implements backtesting, and provides predictions. The project uses AWS for deployment, Docker for containerization, and GitHub for version control and CI/CD.

## Features
- Fetch stock data from public APIs (https://www.alphavantage.co/documentation/)
- Perform stock market backtesting (return , max drawdown, number of trades)
- Train and predict stock prices using machine learning models (linear regression model using sklearn)
- Store stock data in PostgreSQL database (hosted on AWS RDS)
- Dockerized deployment with CI/CD pipeline using GitHub Actions

## Set up project 
- Navigate to my project directory

  
  cd /path/to/my/project

- Create a virtual environment


  python -m venv venv

- Activate the virtual environment


  source venv/bin/activate

- set up database 



  **DATABASE_URL=postgres://postgres:postgres1234@finance.c76e00gyuu66.us-east-2.rds.amazonaws.com:5432/finance**

- Set up models in models.py


  Stock, UserRule and StockPrediction

- running migration

  
  python manage.py makemigrations
  python manage.py migrate

- running server


    python manage.py migrate


    python manage.py runserver


- Access urls


  access data over the past two years: http://127.0.0.1:8000/ [/br]
  access backtest: http://127.0.0.1:8000/backtest
  access prediction for the next 30 days: http://127.0.0.1:8000/predict_stock


