from django.contrib import admin
from . models import *
from .models import Product



class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','preview_text','category', 'created_at')
    search_fields = ('name','preview_text','category', 'created_at')

    def set_price_to_one(self,request,queryset):
        queryset.update(price=1)

    actions =('set_price_to_one',)
    list_editable = ('price','preview_text','created_at')


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)

