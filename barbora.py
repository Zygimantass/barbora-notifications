import requests
import logging
from fake_useragent import UserAgent

API_URL = "https://www.barbora.lt/api/eshop/v1/"
HEADERS = {
    "Host": "www.barbora.lt",
    "Origin": "https://www.barbora.lt",
    "Referer": "https://www.barbora.lt/",
    "X-Requested-With": "XMLHttpRequest",
    "Authorization": "Basic YXBpa2V5OlNlY3JldEtleQ==",
}

class Barbora:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
        self.logger = logging.getLogger("barbora_notifications.api")
        self.logger.setLevel(logging.DEBUG)

        self.session = requests.Session()
        self.session.headers.update({'User-Agent': UserAgent().random})
        self.session.headers.update(HEADERS)
        self.session.get("https://www.barbora.lt")

    def __get(self, endpoint):
        response = self.session.get(API_URL + endpoint)
        return response 

    def __post(self, endpoint, data):
        response = self.session.post(API_URL + endpoint, data=data)
        return response
    
    def login(self):
        self.logger.info("Trying to login")
        login_data = {
            "email": self.username,
            "password": self.password,
            "rememberMe": "true",
        }
        response = self.__post("user/login", login_data)
        
        if response.status_code != 200:
            self.logger.error("Cannot login to Barbora: " + response.text)
            return False
        
        self.logger.info("Successfully logged in")
        return True
    
    def get_deliveries(self):
        self.logger.info("Getting available deliveries")
        response = self.__get("cart/deliveries")

        if response.status_code != 200:
            self.logger.error("Cannot get available deliveries: " + response.text)
            return None 

        return response.json()
    
    def reserve_delivery_time(self, dayId, hourId):
        self.logger.info("Reserving delivery time at {0}, id: {1}".format(dayId, hourId))
        delivery_data = {
            "dayId": dayId,
            "hourId": hourId,
            "isExpressDeliveryTimeslot": "false"
        }

        response = self.__post("cart/ReserveDeliveryTimeSlot", delivery_data)

        if response.status_code != 200:
            self.logger.error("Failed to reserve time slot: " + response.text)
            return False

        self.logger.info("Successfully reserved time slot")
        return True
