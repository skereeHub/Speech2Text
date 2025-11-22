import time
from functools import wraps
import logging


LOGGER = logging.getLogger('Benchmark')


def benchmark(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        LOGGER.debug(f'Function {func.__name__} took {end - start} seconds')
        return result
    return wrapper