import requests
import logging
import config

from logging.handlers import RotatingFileHandler

from notifiers.print_notifier import PrintNotifier
from notifiers.telegram_notifier import TelegramNotifier

from barbora import Barbora
from checker import Checker

logger = logging.getLogger("barbora_notifications")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(levelname)s] [%(name)s] [%(asctime)s] - %(message)s")

stream_handler = logging.StreamHandler()
rotating_handler = RotatingFileHandler("/var/log/barbora.log", maxBytes=1000000, backupCount=20)

stream_handler.setLevel(logging.DEBUG)
rotating_handler.setLevel(logging.DEBUG)

stream_handler.setFormatter(formatter)
rotating_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(rotating_handler)

def get_telegram_notifier():
    return TelegramNotifier(config.TELEGRAM_TOKEN, config.TELEGRAM_GROUP_ID)

def get_print_notifier():
    return PrintNotifier("Notification: {0}")

def get_notifiers():
    return [get_print_notifier(), get_telegram_notifier()]

def main():
    barbora_instance = Barbora(config.USERNAME, config.PASSWORD)

    checker = Checker(barbora_instance, get_notifiers())
    
    delivery = checker.check_deliveries()

    if not delivery:
        logger.info("No deliveries found at this time")
        return

    d_time = delivery['deliveryTime'].replace("T", " ")
    picking_time = delivery['pickingHour']
    
    checker.notify("There is an available delivery time at {0}, the products are going to be picked at {1} hour, will try to reserve".format(d_time, picking_time))
    
    reservation_success = barbora_instance.reserve_delivery_time(delivery['deliveryTime'].split("T")[0], delivery["id"])
    if not reservation_success:
        checker.notify("The reservation failed, there was probably a conflicting reservation, try to check online!")
        return

    checker.notify("Successfully reserved, go order online!")

if __name__ == "__main__":
    main()
