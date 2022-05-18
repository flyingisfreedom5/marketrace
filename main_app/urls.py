from unicodedata import name
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('stocks/', views.stock_index, name='stock'),
    path('stocks/<int:stock_id>/', views.stock_detail, name='stock_detail'),
    path('buckets/create/', views.BucketCreate.as_view(), name='buckets_create'),
    path('buckets/', views.buckets_index, name='buckets_index'),
    path('buckets/<int:bucket_id>/', views.bucket_detail, name='bucket_detail'),
    path('buckets/<int:pk>/delete/', views.BucketDelete.as_view(), name='buckets_delete'),
    path('buckets/<int:pk>/update/', views.BucketUpdate.as_view(), name='buckets_update'),
    path('stocks/<int:stock_id>/stock_inst_create', views.stock_inst_create, name='stock_inst_create'),
]