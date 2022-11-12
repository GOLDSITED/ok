from django.urls import path
from . views import checkout,payment
from . import views
app_name = "checkout"

urlpatterns = [
	path('checkout/', checkout, name="index"),
    path('payment/', payment, name="payment"),
    path('order/', payment, name="order"),
    path('success/',views.PaymentSuccessView.as_view(), name='success'),
    path('failed/',views.PaymentFailedView.as_view(), name='failed'),
    
]