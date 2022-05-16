from django.shortcuts import render, redirect
import os
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import requests
from .models import Stock

# Stock = [{'ticker': 'APPL', 'price': 100, 'description': 'This is a description of words and stuff for APPL'}, {'ticker': 'MSFT', 'price': 200, 'description': 'This is a description of words and stuff for MSFT'}, {'ticker': 'FB', 'price': 10, 'description': 'This is a description of words and stuff for FB'}]

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def signup(request):
    error_message=''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('stock')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


ticker_arr = ['AAPL']


@login_required
def stock_index(request):
    for ticker in ticker_arr:
        stock_data_raw = requests.get(f'https://api.polygon.io/v1/open-close/{ticker}/2022-05-13?adjusted=true&apiKey=ISRFyZyx4zGrz0Pzy3veu6ou4pPUYQjU').json()
        stock_ticker = ticker
        stock_mr_close = stock_data_raw['close']
        stock_mr_volume = stock_data_raw['volume']
    
    currStock = Stock.objects.filter(ticker=ticker)

    if (len(currStock) == 0):
        Stock.objects.create(
            ticker = stock_ticker,
            industry = 'na',
            logo = 'na',
            description = 'na',
            mr_close = stock_mr_close,
            mr_volume = stock_mr_volume,
            market_cap = 1
        )
    else:
        currStock.mr_close = stock_mr_close
        currStock.mr_volume = stock_mr_volume
    
    stocks = Stock.objects.all()
    return render(request,'stock_index.html', {'stocks': stocks})


    # class Stock(models.Model):
    # ticker = models.CharField(max_length=10)
    # industry = models.CharField(max_length=50)
    # logo = models.URLField(max_length=300)
    # description = models.CharField(max_length=2500)

    # mr_close = models.PositiveIntegerField()
    # mr_volume = models.PositiveIntegerField()
    # market_cap = models.PositiveBigIntegerField()