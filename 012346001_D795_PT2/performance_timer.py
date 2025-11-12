import time

def Timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"\nTotal execution time: {time.time() - start:.2f} seconds")
        return result
    return wrapper
