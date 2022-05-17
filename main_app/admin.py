from django.contrib import admin

# Register your models here.
from .models import Stock, Bucket, StockInstance

admin.site.register(Stock)
admin.site.register(Bucket)
admin.site.register(StockInstance)