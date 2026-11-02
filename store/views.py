from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
import re
import uuid
from .cart import Cart
from .models import Order, OrderItem, Product, Category

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(stock__gt=0)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    return render(request, 'store/product_list.html', {
        'products': products, 
        'categories': categories,
        'category': category
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    if product.stock > 0:
        cart.add(product=product)
        messages.success(request, f"محصول '{product.title}' به سبد خرید اضافه شد.")
    else:
        messages.error(request, "متأسفانه این محصول موجودی ندارد.")
        
    return redirect(request.META.get('HTTP_REFERER', 'store:product_list'))

def cart_update(request, product_id, action):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    product_id_str = str(product.id)
    if product_id_str in cart.cart:
        qty = cart.cart[product_id_str]['quantity']
        
        if action == 'increase' and qty < product.stock:
            cart.add(product=product, quantity=qty+1, update_quantity=True)
        elif action == 'decrease' and qty > 1:
            cart.add(product=product, quantity=qty-1, update_quantity=True)
            
    return redirect('store:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('store:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart_detail.html', {'cart': cart})

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('store:product_list')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        address = request.POST.get('address', '').strip()
        phone = request.POST.get('phone', '')

        full_name = f"{first_name} {last_name}".strip()
        total_price = cart.get_total_price() 

        if not address:
            messages.error(request, 'لطفاً آدرس پستی خود را وارد کنید.')
            return render(request, 'store/checkout.html', {'cart': cart})

        user = request.user if request.user.is_authenticated else None

        order = Order.objects.create(
            user=user,
            full_name=full_name, 
            address=address, 
            phone=phone, 
            total_price=total_price
        )

        for item in cart:
            OrderItem.objects.create(
                order=order, 
                product=item['product'], 
                price=item['price'], 
                quantity=item['quantity']
            )
            # کسر از موجودی انبار
            product = item['product']
            product.stock -= item['quantity']
            product.save()

        return redirect('store:payment', order_id=order.id)

    return render(request, 'store/checkout.html', {'cart': cart})

def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        card_number = request.POST.get('card_number', '')
        cvv2 = request.POST.get('cvv2', '')
        
        # اعتبارسنجی شماره کارت (16 رقم) و CVV2 (3 یا 4 رقم)
        if re.match(r'^\d{16}$', card_number) and re.match(r'^\d{3,4}$', cvv2):
            # پرداخت موفق
            order.status = 'success'
            order.tracking_code = str(uuid.uuid4().hex[:10].upper())
            order.save()
            
            # خالی کردن سبد خرید
            Cart(request).clear()
            return render(request, 'store/payment_result.html', {'order': order, 'success': True})
        else:
            # پرداخت ناموفق
            order.status = 'failed'
            order.save()
            
            # برگرداندن موجودی به انبار
            for item in order.items.all():
                product = item.product
                product.stock += item.quantity
                product.save()
            
            Cart(request).clear()
            return render(request, 'store/payment_result.html', {'order': order, 'success': False})

    return render(request, 'store/payment.html', {'order': order})