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
from .models import Stock, StockInstance
from .forms import StockForm, StockFormMod
from django.contrib.auth.models import User
from api_call import *

def home(request):
    user = request.user
    if user.is_superuser:
        runFunc()
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
    bucket = Bucket(user = request.user)
    buckets = Bucket.objects.filter(user = request.user)

    stock_form = StockForm(data = request.POST or None, instance=bucket, user=request.user)

    message = ''
    stock_logo = ''
    # Pull stock logo
    stock_data_raw = requests.get(f'https://api.polygon.io/v3/reference/tickers/{stock.ticker}?apiKey=ISRFyZyx4zGrz0Pzy3veu6ou4pPUYQjU').json()
    
    keyResults = 'results'
    key = 'branding'
    keyTwo = 'logo_url'
    if keyResults in stock_data_raw:
        if key in stock_data_raw[keyResults]:
            if keyTwo in stock_data_raw[keyResults][key]:
                stock_logo = (f"{stock_data_raw['results']['branding']['logo_url']}?apiKey=ISRFyZyx4zGrz0Pzy3veu6ou4pPUYQjU")
    else:
        message = 'Unable to render image'
    print(f'logo - {stock_logo}')
    return render(request, 'stock_detail.html', {
        'stock': stock, 
        'stock_form': stock_form,
        'buckets': buckets,
        'stock_logo': stock_logo,
        'message': message
    })


# ticker_arr = ['AAPL', 'GOOGL' ]


@login_required
def stock_index(request):
    
    stocks = Stock.objects.all()
    return render(request,'stock_index.html', {'stocks': stocks})



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


@login_required
def bucket_detail(request, bucket_id):
    bucket = Bucket.objects.get(id = bucket_id)
    stocks = StockInstance.objects.filter(bucket = bucket_id)
    
    totalReturn = 0
    totalCount = 0

    for stock in stocks:
        totalCount +=1
        totalReturn += (  (stock.stock.mr_close/stock.price) -1  ) * 100
    
    stock_form = StockFormMod()

    bucketReturn = round(totalReturn / totalCount, 2) if totalCount > 0 else 0
    return render(request, 'main_app/bucket_detail.html', {
        'bucket': bucket,
        'stocks': stocks,
        'bucketReturn': bucketReturn, 
        'stock_form': StockFormMod()
        })



# class BucketDetail(LoginRequiredMixin, DetailView):
#     model = Bucket
#     fields = '__all__'

class BucketDelete(LoginRequiredMixin, DeleteView):
  model = Bucket
  success_url = '/buckets/'


class BucketUpdate(LoginRequiredMixin, UpdateView):
  model = Bucket
  fields = ['name']
  success_url = '/buckets/'

@login_required
def stock_inst_create(request, stock_id):
    form = StockForm(request.POST, user=request.user)
    if form.is_valid():
        new_stockInst = form.save(commit = False)
        new_stockInst.price = form.cleaned_data.get('stock').mr_close
        new_stockInst.save()

    return redirect('buckets_index')

@login_required
def stock_inst_create_bucket(request, bucket_id):
    form = StockFormMod(request.POST)
    if form.is_valid():
        new_stockInst = form.save(commit = False)
        new_stockInst.price = form.cleaned_data.get('stock').mr_close
        new_stockInst.bucket = Bucket.objects.get(id = bucket_id)
        new_stockInst.save()

    return redirect('bucket_detail', bucket_id=bucket_id)

@login_required
def stock_inst_delete(request, stock_id):
    bucket = StockInstance.objects.get(pk = stock_id).bucket
    StockInstance.objects.get(pk = stock_id).delete()
    return redirect('bucket_detail', bucket_id = bucket.id)