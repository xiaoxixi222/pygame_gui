import logging


logging.basicConfig(
    level=logging.DEBUG,
    filename="example.log",
    filemode="w",
    encoding="utf-8",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)