from fee import quote

cases = [
    ("regular", 1, 300),
    ("regular", 2, 600),
    ("regular", 3, 810),
    ("student", 3, 540),
    ("student", 4, 720),
]
for kind, quantity, expected in cases:
    assert quote(kind, quantity) == expected, (kind, quantity)

for kind, quantity in [
    ("vip", 1), ("regular", 0), ("student", -1),
    ("regular", 1.5), ("student", True), ("regular", "3")
]:
    try:
        quote(kind, quantity)
    except ValueError:
        pass
    else:
        raise AssertionError((kind, quantity))
print("ACCEPTED: fee contract")
