from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_stock_data, name='list_stock_data'), 
    path('backtest/', views.backtest, name='backtest'), 
    path('predict_stock/', views.predictStock, name='predictStock'),

]