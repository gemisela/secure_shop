from django.shortcuts import render,redirect,get_object_or_404
from .models import Product

def home(request): return render(request,'shop/home.html')
def products(request): return render(request,'shop/products.html',{'products':Product.objects.all()})
def add_cart(request,pk):
 p=get_object_or_404(Product,pk=pk); cart=request.session.get('cart',{}); cart[str(pk)]=cart.get(str(pk),0)+1; request.session['cart']=cart; return redirect('cart')
def cart(request):
 cart=request.session.get('cart',{}); items=[]; total=0
 for p in Product.objects.filter(id__in=cart.keys()):
  q=cart[str(p.id)]; sub=p.price*q; total+=sub; items.append((p,q,sub))
 return render(request,'shop/cart.html',{'items':items,'total':total})
def clear_cart(request): request.session['cart']={}; return redirect('cart')
