from cbpro.authenticated_client import AuthenticatedClient
from Data import Path


class Order:
    """
    Class that stores the data from Authenticated.get_order() in a dictionary
    to facilitate its use

    Example of AuthenticatedClient.get_order():
    {
        "id": "68e6a28f-ae28-4788-8d4f-5ab4e5e5ae08",
        "size": "1.00000000",
        "product_id": "BTC-USD",
        "side": "buy",
        "stp": "dc",
        "funds": "9.9750623400000000",
        "specified_funds": "10.0000000000000000",
        "type": "market",
        "post_only": false,
        "created_at": "2016-12-08T20:09:05.508883Z",
        "done_at": "2016-12-08T20:09:05.527Z",
        "done_reason": "filled",
        "fill_fees": "0.0249376391550000",
        "filled_size": "0.01291771",
        "executed_value": "9.9750556620000000",
        "status": "done",
        "settled": true
    }
    """

    def __init__(self, client=AuthenticatedClient):
        """
        Creates an instance of Order

        :param client: instance of AuthenticatedClient
        """

        self.client = client
        self.new_id = None
        self.is_bottom = False
        self.is_raising = False
        self.is_top = False
        self.is_falling = False
        self.details = {
            "id": "",
            "size": "",
            "product_id": "",
            "side": "",
            "stp": "",
            "funds": "",
            "specified_funds": "",
            "type": "",
            "post_only": None,
            "created_at": "",
            "done_at": "",
            "done_reason": "",
            "fill_fees": "",
            "filled_size": "",
            "executed_value": "",
            "status": "",
            "settled": None
        }

    def set_details(self):
        """
        Makes sure that the response contains a valid request

        :return: Whether the response is valid
        """
        confirm = False
        while confirm is False:
            self.details = self.client.get_order(order_id=self.new_id)
            if 'status' in self.details:
                if self.details['status'] == 'done':
                    confirm = True
            return confirm

    def get_key(self, key):
        """
        returns the value mapped to parameter

        :param key: value to get the mapped value from

        :return: The mapped value or None
        """

        return self.details[key]

    def get_id(self):
        """
        Opens a file where the Coibase order ID number is stored and saves it in a variable

        :return: The Id number for the latest trade executed
        """
        writer = open(Path, 'r')
        self.new_id = writer.read()
        writer.close()
        return self.new_id

    def get_bottom(self):
        return self.is_bottom

    def get_rise(self):
        return self.is_raising

    def get_top(self):
        return self.is_top

    def get_fall(self):
        return self.is_falling
