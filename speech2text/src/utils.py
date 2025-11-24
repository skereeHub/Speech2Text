import time
from functools import wraps
import logging
import re
from datetime import datetime


LOGGER = logging.getLogger('Benchmark')


def benchmark(func):
    """
    Время выполнения функции
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        LOGGER.debug(f'Function {func.__name__} took {end - start} seconds')
        return result
    return wrapper

def date_from_filename(filename: str) -> str:
    """
    Парсим дату из файла
    """
    match = re.search(
        r'\d{4}-\d{2}-\d{2}',
        filename
    )
    return match.group()