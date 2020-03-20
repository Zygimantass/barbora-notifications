import requests
import logging
import config

from barbora import Barbora
from checker import Checker

logging.basicConfig(format="[%(levelname)s] [%(name)s] [%(asctime)s] - %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def main():
    barbora_instance = Barbora(config.USERNAME, config.PASSWORD)
    checker = Checker(barbora_instance, [])
    checker.check_deliveries()
if __name__ == "__main__":
    main()
