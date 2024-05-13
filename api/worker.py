import json

def worker(sale):
    sale = dict(sale)

    print(type(sale))
    print(sale)

    categories = {
    "Fruit": ["apple", "banana", "orange", "pear", "kiwi"],
    "Bakery": ["bread", "croissant", "baguette", "cake"],
    "Drink": ["water", "soda", "beer", "wine"]
    }

    total_price = 0
    category = ""
    for item in sale['items']:
        total_price += item['price']
        sale['total_price'] = total_price
        for cat, it in categories.items():
            if item['product'] in it:
                category = cat
                item['category'] = cat
                break

    return sale

