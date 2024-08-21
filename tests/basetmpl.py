from unittest import TestCase
import sys, io, logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt='%B %d, %Y %H:%M:%S'
)

class TestTmpl(TestCase):
    def setUp(self):
        logging.info('=' * 60)
        logging.info(f"{self.id()} start")

    def tearDown(self):
        logging.info(f'{self.id()} finish')
