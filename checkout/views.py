from django.shortcuts import render, get_object_or_404, redirect
from . models import BillingForm, BillingAddress
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.utils.crypto import get_random_string
import stripe
from django.conf import settings
from cartes.models import Order

stripe.api_key = settings.STRIPE_KEY

# Create your views here.

def checkout(request):

	# Checkout view
	form = BillingForm

	order_qs = Order.objects.filter(user= request.user, ordered=False)
	order_items = order_qs[0].orderitems.all()
	order_total = order_qs[0].get_totals()
	context = {"form": form, "order_items": order_items, "order_total": order_total}
	# Getting the saved saved_address
	saved_address = BillingAddress.objects.filter(user = request.user)
	if saved_address.exists():
		savedAddress = saved_address.first()
		context = {"form": form, "order_items": order_items, "order_total": order_total, "savedAddress": savedAddress}
	if request.method == "POST":
		saved_address = BillingAddress.objects.filter(user = request.user)
		if saved_address.exists():

			savedAddress = saved_address.first()
			form = BillingForm(request.POST, instance=savedAddress)
			if form.is_valid():
				billingaddress = form.save(commit=False)
				billingaddress.user = request.user
				billingaddress.save()
		else:
			form = BillingForm(request.POST)
			if form.is_valid():
				billingaddress = form.save(commit=False)
				billingaddress.user = request.user
				billingaddress.save()

	return render(request, 'checkout/index.html', context)


def payment(request):
	key = settings.STRIPE_PUBLISHABLE_KEY
	order_qs = Order.objects.filter(user= request.user, ordered=False)
	order_total = order_qs[0].get_totals()
	totalCents = float(order_total * 100);
	total = round(totalCents, 2)
	if request.method == 'POST':
		charge = stripe.Charge.create(amount=total,
            currency='usd',
            description=order_qs,
            source=request.POST['stripeToken'])


	return render(request, 'checkout/payment.html', {"key": key, "total": total})



def charge(request):
	order = Order.objects.get(user=request.user, ordered=False)
	order_total = order.get_totals()
	totalCents = int(float(order_total * 100));
	if request.method == 'POST':
		charge = stripe.Charge.create(amount=totalCents,
            currency='usd',
            description=order,
            source=request.POST['stripeToken'])
		if charge.status == "succeeded":
			orderId = get_random_string(length=16, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
			print(charge.id)
			order.ordered = True
			order.paymentId = charge.id
			order.orderId = f'#{request.user}{orderId}'
			order.save()
			cartItems = Cart.objects.filter(user=request.user)
			for item in cartItems:
				item.purchased = True
				item.save()
		return render(request, 'checkout/charge.html')


def orderView(request):

	try:
		orders = Order.objects.filter(user=request.user, ordered=True)
		context = {
			"orders": orders
		}
	except:
		messages.warning(request, "You do not have an active order")
		return redirect('/')
	return render(request, 'checkout/order.html', context)


class PaymentSuccessView(TemplateView):
    template_name ='checkout/payment_success.html'

    def get(self,request,*args,**kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        session = stripe.checkout.Session.retrieve(session_id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = get_object_or_404(OrderDetail,stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request,self.template_name)

class PaymentFailedView(TemplateView):
    template_name = 'checkout/payment_failed.html'
