def make_label(name, seats):
    return f"{name.strip()}｜{seats} 位"


if __name__ == "__main__":
    print(make_label(" 林青 ", 2))