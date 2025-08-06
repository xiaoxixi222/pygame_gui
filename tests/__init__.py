import logging
import sys, os

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)
logging.basicConfig(
    level=logging.DEBUG,
    filename="example.log",
    filemode="w",
    encoding="utf-8",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
