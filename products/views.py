from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .filters import ProductFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django_filters.views import FilterView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.urls import reverse,reverse_lazy
from . forms import ProductForm

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from .models import  Product,Category
from . forms import ProductForm
import datetime



def products(request):    
    page_obj =  products = Product.objects.all()

    product_name = request.GET.get('product_name')
    if product_name!='' and product_name is not None:
        page_obj = products.filter(name__icontains=product_name)

    paginator = Paginator(page_obj,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context={
        'page_obj':page_obj

        
    }
    return render(request, 'products/home.html',context)

class Home(ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = 'home'
    filterset_class = ProductFilter
    paginate_by = 4


    def get_context_data(self, **kwargs):       
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())       
        return context

def home(request):
    product_list = Product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=product_list)
    return render(request, 'products/home.html', {'filter': product_filter})


def addProduct(request):
    form = ProductForm()

    if request.method =='POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('products:home')
    else:
        form = ProductForm()

    context = {
        "form":form
    }
    return render(request, 'products/addproduct.html', context)

class ProductDetail(LoginRequiredMixin, DetailView):
	model = Product

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name','price','preview_text','image','seller_name']
    template_name_suffix = '_update_form'

class ProductCreateView(CreateView):
    model = Product
    fields = [ 'seller_name','image','name','slug','category','preview_text','detail_text','image','price']
    #product_form.html


def delete_product(request,id):
    product = Product.objects.get(id=id)
    context={
        'product':product,
    }
    if request.method =='POST':
        product.delete()
        return redirect('/products/products')
    return render (request,'products/delete.html',context)

class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('products:home')



def my_listings(request):
        products = Product.objects.filter(seller_name=request.user)
        context ={
            'products':products,
        }
        return render(request,'products/mylistings.html',context)



def about(request):
    return render(request,'products/about.html')


def product_list(request):
    product_list = Wine.objects.order_by('-name')
    context = {'product_list':product_list}
    return render(request, 'products/product_list.html', context)



def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'products/product_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'products/product_detail.html', {'review': review})


def product_list(request):
    product_list = Product.objects.order_by('-name')
    context = {'product_list':product_list}
    return render(request, 'products/product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=wine_id)
    form = ReviewForm()
    return render(request, 'products/product_detail.html', {'product': product, 'form': form})


def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = form.cleaned_data['user_name']
        review = Review()
        review.product = product
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('products:product_detail', args=(slug.id,)))

    return render(request, 'products/product_detail.html', {'product': product, 'form': form})
    
  