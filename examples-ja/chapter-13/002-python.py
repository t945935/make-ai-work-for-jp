def quote(kind, quantity):
    prices = {"regular": 300, "student": 200}
    if kind not in prices:
        raise ValueError("unknown ticket kind")
    if type(quantity) is not int or quantity < 1:
        raise ValueError("quantity must be a positive integer")
    return prices[kind] * quantity
