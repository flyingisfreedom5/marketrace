from django.forms import ModelForm, ModelChoiceField
from django import forms
from django.contrib.auth.models import User
from .models import Stock, Bucket, StockInstance




class StockForm(ModelForm):
  
  class Meta:
    model = StockInstance
    fields = ['bucket']

  def __init__(self, *args, **kwargs):
          user = kwargs.pop('user')
          super(StockForm, self).__init__(*args, **kwargs)
          if self.instance:
              self.fields['bucket'].queryset = Bucket.objects.filter(user = user)


class StockFormMod(ModelForm):
  class Meta:
    model = StockInstance
    fields = ['stock']


      