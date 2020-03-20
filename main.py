import requests
import logging
import config

from notifiers.print_notifier import PrintNotifier
from barbora import Barbora
from checker import Checker

logging.basicConfig(format="[%(levelname)s] [%(name)s] [%(asctime)s] - %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_print_notifier():
    return PrintNotifier("Notification: {0}")

def get_notifiers():
    return [get_print_notifier()]

def main():
    barbora_instance = Barbora(config.USERNAME, config.PASSWORD)

    checker = Checker(barbora_instance, get_notifiers())
    
    delivery = checker.check_deliveries()

    if not delivery:
        logger.info("No deliveries found at this time")
        return

    d_time = delivery['deliveryTime'].replace("T", " ")
    picking_time = delivery['pickingHour']

    checker.notify("There is an available delivery time at {0}, the products are going to be picked at {1} hour".format(d_time, picking_time))

if __name__ == "__main__":
    main()
