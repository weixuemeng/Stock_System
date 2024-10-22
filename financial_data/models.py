from django.db import models

# Create your models here.
class Stock(models.Model):
    stock_symbol = models.CharField(max_length=20)
    open_price = models.DecimalField(max_digits=10, decimal_places=4)
    close_price = models.DecimalField(max_digits=10, decimal_places=4)
    high_price = models.DecimalField(max_digits=10, decimal_places=4)
    low_price = models.DecimalField(max_digits=10, decimal_places=4)
    time_stamp = models.DateField()
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('stock_symbol', 'time_stamp')
        ordering = ('time_stamp',)

class UserRule(models.Model):
    initial_investment = models.DecimalField(max_digits=10, decimal_places=4)
    buy_avg = models.PositiveIntegerField()
    sell_avg = models.PositiveIntegerField()
    post_time = models.DateTimeField(auto_now_add=True)

class StockPrediction(models.Model):
    date = models.DateField()
    predicted_price = models.FloatField()



