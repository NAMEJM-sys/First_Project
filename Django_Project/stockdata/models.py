from django.db import models

class StockData(models.Model):
    stock_code = models.CharField(max_length=10)
    stock_name = models.CharField(max_length=100)
    close_price = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.date} -{self.close_price}"


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.username