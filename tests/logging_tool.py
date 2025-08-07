import time
import unittest
import logging


def logging_tool(test: type[unittest.TestCase]):
    logging.debug(f"test case:{test.__dict__}")
    for i in test.__dict__:
        if i.startswith("test_"):
            wrapper = log(getattr(test, i))
            setattr(test, i, wrapper)
    return test


def log(func):
    def wrapper(self, *args, **kwargs):
        logging.info(f"{func.__name__}:start")
        t = time.time()
        func(self, *args, **kwargs)
        logging.info(f"{func.__name__}:end, time:{int((time.time()-t)*1000)}ms")

    return wrapper
