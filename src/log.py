import logging

from src.config import LOGS_DIR


def initialize_logging(filename: str):
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                        datefmt='%Y-%d-%m %I:%M:%S',
                        level=logging.INFO,
                        handlers=[logging.FileHandler(filename), logging.StreamHandler()])