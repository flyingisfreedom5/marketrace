from django.shortcuts import render, redirect
import os
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

Stock = [{'ticker': 'APPL', 'price': 100, 'description': 'This is a description of words and stuff for APPL'}, {'ticker': 'MSFT', 'price': 200, 'description': 'This is a description of words and stuff for MSFT'}, {'ticker': 'FB', 'price': 10, 'description': 'This is a description of words and stuff for FB'}]

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def stock_index(request):
    stocks = Stock
    return render(request,'stock_index.html', {'stocks': stocks})

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