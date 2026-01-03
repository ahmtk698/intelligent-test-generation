def calculate_cart_total(cart_items, user_type="guest"):
    """Calculate the total price of the cart (Handling List and Dictionary)."""
    if type(cart_items) != list:
        raise TypeError("Cart items must be a list")
    
    total = 0.0
    for item in cart_items:
        if type(item) != dict or 'price' not in item or 'qty' not in item:
            continue
        price = item['price']
        qty = item['qty']
        if price < 0 or qty < 0:
            raise ValueError("Price and quantity must be non-negative")
        total += price * qty

    if total == 0: return 0.0

    if user_type == "gold": total *= 0.80
    elif user_type == "silver": total *= 0.90
        

    if total >= 1000: total -= 50
        
    return round(max(0.0, total), 2)