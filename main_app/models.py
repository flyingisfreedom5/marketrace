from pydoc import describe
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    industry = models.CharField(max_length=50)
    logo = models.URLField(max_length=300)
    description = models.CharField(max_length=2500)

    mr_close = models.PositiveIntegerField()
    mr_volume = models.PositiveIntegerField()
    market_cap = models.PositiveBigIntegerField()


    def __str__(self):
        return f'{self.ticker} - Price: {self.mr_close}'

class Bucket(models.Model):
    name = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add = True)
    numStocks = models.IntegerField(default = 0)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )    

    def __str__(self):
        return f'{self.name}'


class StockInstance(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.IntegerField()
    date = models.DateTimeField(auto_now_add = True)
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)

    def __str__(self):
        return f'Stock Instance of {self.stock.ticker}'



        


