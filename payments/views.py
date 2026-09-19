from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.utils import timezone
from shop.models import Product
from .models import Transaction
from .security import generate_nonce,sign,verify

def cart_data(request):
 cart=request.session.get('cart',{}); items=[]; total=Decimal('0')
 for p in Product.objects.filter(id__in=cart.keys()):
  q=cart[str(p.id)]; sub=p.price*q; total+=sub; items.append((p,q,sub))
 return items,total
@login_required
def checkout(request):
 items,total=cart_data(request)
 if not items:return redirect('products')
 return render(request,'payments/checkout.html',{'items':items,'total':total})
@login_required
def process(request):
 if request.method!='POST': return redirect('checkout')
 items,total=cart_data(request)
 if not items:return redirect('products')
 nonce=generate_nonce(); ref='PAY-'+timezone.now().strftime('%Y%m%d%H%M%S%f')[:20]; signature=sign(ref,str(total),nonce)
 if Transaction.objects.filter(nonce=nonce).exists() or not verify(ref,str(total),nonce,signature): return render(request,'payments/failed.html')
 tx=Transaction.objects.create(user=request.user,reference=ref,amount=total,nonce=nonce,hmac_signature=signature)
 request.session['cart']={}; return render(request,'payments/success.html',{'tx':tx,'items':items})
