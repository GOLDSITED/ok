from django.forms import ModelForm, Textarea
from django import forms
from . models import Product



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['seller_name','image','name','slug','category','preview_text','price','is_published']
    