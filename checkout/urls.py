from django.urls import path
from . views import checkout,payment

app_name = "checkout"

urlpatterns = [
	path('checkout/', checkout, name="index"),
    path('payment/', payment, name="payment"),
]