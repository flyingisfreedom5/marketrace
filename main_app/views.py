from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
import os
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import requests
from main_app.models import Bucket
from .models import Stock
from .forms import StockForm

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


@login_required
def stock_detail(request, stock_id):
    stock = Stock.objects.get(id = stock_id)
    stock_form = StockForm()
    return render(request, 'stock_detail.html', {
        'stock': stock, 'stock_form': stock_form

    })


# ticker_arr = ['AAPL', 'GOOGL' ]


@login_required
def stock_index(request):
    # for ticker in ticker_arr:
    #     stock_data_raw = requests.get(f'https://api.polygon.io/v1/open-close/{ticker}/2022-05-13?adjusted=true&apiKey=ISRFyZyx4zGrz0Pzy3veu6ou4pPUYQjU').json()
    #     stock_ticker = ticker
    #     stock_mr_close = stock_data_raw['close']
    #     stock_mr_volume = stock_data_raw['volume']
    
    # currStock = Stock.objects.filter(ticker=ticker)

    # if (len(currStock) == 0):
    #     Stock.objects.create(
    #         ticker = stock_ticker,
    #         industry = 'na',
    #         logo = 'na',
    #         description = 'na',
    #         mr_close = stock_mr_close,
    #         mr_volume = stock_mr_volume,
    #         market_cap = 1
    #     )
    # else:
    #     currStock.mr_close = stock_mr_close
    #     currStock.mr_volume = stock_mr_volume
    
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

class BucketCreate(LoginRequiredMixin, CreateView):
    model = Bucket
    fields = ['name']
    success_url = '/buckets/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def buckets_index(request):
  buckets = Bucket.objects.filter(user=request.user)
  return render(request, 'main_app/buckets_index.html', {'buckets': buckets})


# class BucketList(LoginRequiredMixin, ListView):
#     model = Bucket

class BucketDetail(LoginRequiredMixin, DetailView):
    model = Bucket
    fields = '__all__'

class BucketDelete(LoginRequiredMixin, DeleteView):
  model = Bucket
  success_url = '/buckets/'

class BucketUpdate(LoginRequiredMixin, UpdateView):
  model = Bucket
  fields = ['name']
  success_url = '/buckets/'

def stock_inst_create(request):
    form = StockForm(request.POST)
    if form.is_valid():
        new_stockInst = form.save(commit = False)
        new_stockInst.price = Stock.objects.get(pk = form.stock.id).mr_close
        new_stockInst.save()
    return redirect('buckets_detail', bucket_id = form.bucket.id)