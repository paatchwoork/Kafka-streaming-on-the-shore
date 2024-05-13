from datetime import date as dt
import numpy as np
import random
import json

class Sale:
    def __init__(self):
        stores = {1000: "Brussels", 2000: "Antwerp", 3000: "Liege", 4000: "Namur", 5000: "Gent"}

        self.store, self.store_id = random.choice(list(stores.items()))
        self.date = str(dt.today())

        self.nb_items = random.randint(1,10)

        raw_items = [Item() for i in range(self.nb_items)]
        self.items = [it.__dict__ for it in raw_items]

class Item:
    def __init__(self):

        products = {
                  "01": "apple", 
                  "02": "banana", 
                  "03": "orange", 
                  "04": "pear", 
                  "05": "kiwi",
                  "06": "bread", 
                  "07": "croissant", 
                  "08": "baguette", 
                  "09": "cake",
                  "10": "water", 
                  "11": "soda", 
                  "12": "beer", 
                  "13": "wine"
                  }

        self.product_id, self.product = random.choice(list(products.items()))
        self.price = 1.5

def producer():
    s = Sale()
    return s.__dict__
