from functools import wraps
import time
import logging

def pipeline_step(func):
    """Decorator to mark a function as a pipeline step"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logging.info(f"Starting pipeline step: {func.__name__}")
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Completed pipeline step: {func.__name__} in {end_time - start_time:.2f}s")
        return result
    return wrapper

def validate_phase(func):
    """Decorator to validate the phase parameter"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Here we could add phase validation if needed
        return func(*args, **kwargs)
    return wrapper