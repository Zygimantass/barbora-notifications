import logging
from notifiers.notifier import Notifier

class Checker:
    def __init__(self, barbora_instance, notifiers):
        self.barbora = barbora_instance
        self.notifiers = notifiers
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.barbora.login()

    def notify(self, message):
        for notifier in notifiers:
            notifier.notify(message)

    def available_deliveries(self, date_deliveries):
        return list(filter(lambda x: x["available"], date_deliveries))
    
    def have_selected(self, available_deliveries):
        print([x.get('selected', False) for x in available_deliveries])
        return any([x.get('selected', False) for x in available_deliveries])

    def check_deliveries(self):
        self.logger.info("Checking available deliveries")
        deliveries = self.barbora.get_deliveries()
        
        if not deliveries:
            return

        delivery_list = deliveries["deliveries"][0]["params"]["matrix"]
        delivery_list[0]["hours"][0]["available"] = True
        available_deliveries = {day["id"]: self.available_deliveries(day["hours"]) for day in delivery_list}

        for day in available_deliveries:
            if self.have_selected(available_deliveries[day]):
                logger.info("You have already selected a delivery, continuing")
                return
        
            

