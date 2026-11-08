def quote(kind, quantity):
    prices = {"regular": 300, "student": 200}
    if kind not in prices:
        raise ValueError("チケット種別が不明です")
    if type(quantity) is not int or quantity < 1:
        raise ValueError("数量は1以上の整数で指定してください")
    return prices[kind] * quantity
