def cart_count(request):
    cart = request.session.get('cart', {})
    count = 0
    if isinstance(cart, dict):
        for item in cart.values():
            if isinstance(item, dict):
                count += int(item.get('quantity', 0))
            elif isinstance(item, (int, float)):
                count += int(item)
    return {'cart_count': count}
