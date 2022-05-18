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
from .forms import StockForm
from django.contrib.auth.models import User

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
    bucket = Bucket(user = request.user)


    stock_form = StockForm(data = request.POST or None, instance=bucket, user=request.user)



    return render(request, 'stock_detail.html', {
        'stock': stock, 'stock_form': stock_form

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
    
    
    bucketReturn = round(totalReturn / totalCount, 2) if totalCount > 0 else 0
    return render(request, 'main_app/bucket_detail.html', {
        'bucket': bucket,
        'stocks': stocks,
        'bucketReturn': bucketReturn, 
        
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
def stock_inst_delete(request, stock_id):
    bucket = StockInstance.objects.get(pk = stock_id).bucket
    StockInstance.objects.get(pk = stock_id).delete()
    return redirect('bucket_detail', bucket_id = bucket.id)