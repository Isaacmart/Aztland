from cbpro import AuthenticatedClient
from app_methods import get_capital
import Data


class Capital:

    def __init__(self, client=AuthenticatedClient):
        self.client = client
        self.capital = 0.0

    def set_capital(self):
        self.capital = get_capital('42d739b5-f5cd-48c0-baf6-b905836a1ca4', self.client)

    def get_capital(self):
        return float(self.capital) - 1.0







