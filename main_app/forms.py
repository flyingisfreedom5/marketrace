from django.forms import ModelForm
from .models import Stock, Bucket, StockInstance

class StockForm(ModelForm):
  class Meta:
    model = StockInstance
    fields = ['stock', 'bucket']