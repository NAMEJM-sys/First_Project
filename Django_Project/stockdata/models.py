from django.db import models

class StockData(models.Model):
    stock_code = models.CharField(max_length=10)
    stock_name = models.CharField(max_length=100)
    current_price = models.IntegerField()
    trading_volume = models.BigIntegerField()
    date = models.DateField()

    def __str__(self):
        return self.stock_name