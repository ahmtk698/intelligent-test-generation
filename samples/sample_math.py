def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b

def is_even(n):
    return n % 2 == 0