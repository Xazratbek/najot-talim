from functools import reduce, wraps
import time

def code_time(base_func):
    @wraps(base_func)
    def wrapper(*args):
        start_time = time.time()
        print(base_func(*args))
        end_time = time.time()
        return f"Kodni ishlash vaqti: {end_time-start_time}"

    return wrapper

def decorator(func):
    @wraps(func)
    def wrapper(*args):
        data = list(filter(lambda x: x> 0, args))
        return func(*data)
    return wrapper

@code_time
@decorator
def test(*args):
    return reduce(lambda x, y: x + y, args)

print(test(3, 4, 7))
print(test.__name__)