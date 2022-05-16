from unicodedata import name
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('stocks/', views.stock_index, name='stock'),
    path('stocks/<int:stock_id>/', views.stock_detail, name='stock_detail'),
]