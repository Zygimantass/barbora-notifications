import logging
from notifiers.notifier import Notifier

class Checker:
    def __init__(self, barbora_instance, notifiers):
        self.barbora = barbora_instance
        self.notifiers = notifiers
        self.logger = logging.getLogger("barbora_notifications.checker")
        self.logger.setLevel(logging.DEBUG)

        self.barbora.login()

    def notify(self, message):
        for notifier in self.notifiers:
            notifier.notify(message)

    def available_deliveries(self, date_deliveries):
        return list(filter(lambda x: x["available"], date_deliveries))
    
    def have_selected(self, available_deliveries):
        return any([x.get('selected', False) for x in available_deliveries])

    def check_deliveries(self):
        self.logger.info("Checking available deliveries")
        deliveries = self.barbora.get_deliveries()
        
        if not deliveries:
            return

        delivery_list = deliveries["deliveries"][0]["params"]["matrix"]
        available_deliveries_by_day = {day["id"]: self.available_deliveries(day["hours"]) for day in delivery_list}

        for day, deliveries in available_deliveries_by_day.items():
            if self.have_selected(deliveries):
                self.logger.info("You have already selected a delivery, continuing")
                return
        
        for day, deliveries in available_deliveries_by_day.items():
            if len(deliveries) == 0:
                continue
            
            # choose the first available delivery

            return deliveries[0]
        
        return None
            
         

