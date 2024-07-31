from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from cart.cart import Cart
# Create your views here.


def order_create(request):
    cart = Cart(request)
    
    if len(cart) == 0:
        return redirect('shop:product_list')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, user=request.user)
        if form.is_valid():
            
            
            not_in_stock = False
            for item in cart:
                product = item['product']
                if product.stock < item['quantity']:
                    not_in_stock = True
                    break
            
            if not not_in_stock:
                order = form.save()
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                    product = item['product']
                    product.stock -= item['quantity']
                    product.save()
                
                cart.clear()
                return render(request, 'orders/created.html', {'order': order})

            return redirect('orders:order_create')
            
            
    form = OrderCreateForm(user=request.user)
    return render(request, 'orders/create.html', {'form': form, 'cart': cart})