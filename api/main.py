from worker import worker
from producer import producer

sale_raw = producer()
print(type(sale_raw))
print(sale_raw)

sale_clean = worker(sale_raw)
print(type(sale_clean))
print(sale_clean)

