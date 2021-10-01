from cbpro import AuthenticatedClient


class Capital:

    def __init__(self, client=AuthenticatedClient):
        self.client = client
        self.capital = 0.0

    def set_capital(self):
        data = None
        try:
            data = self.client.get_account('42d739b5-f5cd-48c0-baf6-b905836a1ca4')
        except Exception as e:
            print(e)

        self.capital = float(data['available'])

    def get_capital(self):
        return str(self.capital)








