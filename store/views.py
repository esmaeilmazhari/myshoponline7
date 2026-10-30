from django.shortcuts import get_object_or_404, redirect, render
from .cart import Cart
from .models import Order, OrderItem, Product


def product_list(request):
  # نمایش محصولاتی که موجودی انبارشان بیشتر از صفر است
  products = Product.objects.filter(stock__gt=0)
  return render(request, 'store/product_list.html', {'products': products})


def cart_add(request, product_id):
  cart = Cart(request)
  product = get_object_or_404(Product, id=product_id)
  cart.add(product=product)
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
  if request.method == 'POST':
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    address = request.POST.get('address')
    phone = request.POST.get('phone')

    # ایجاد سفارش جدید
    order = Order.objects.create(
        first_name=first_name,
        last_name=last_name,
        address=address,
        phone=phone,
    )

    # انتقال آیتم‌های سبد خرید به سفارش
    for item in cart:
      OrderItem.objects.create(
          order=order,
          product=item['product'],
          price=item['price'],
          quantity=item['quantity'],
      )

    # پاک کردن سبد خرید پس از ثبت سفارش
    cart.clear()
    return render(request, 'store/success.html', {'order': order})

  return render(request, 'store/checkout.html', {'cart': cart})
