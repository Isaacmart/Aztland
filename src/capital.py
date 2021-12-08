from cbpro import AuthenticatedClient


class Capital:

    def __init__(self, client=AuthenticatedClient):
        self.__client = client
        self.__capital: float
        self.__set_capital()

    def __set_capital(self):
        data = None
        try:
            data = self.__client.get_account('42d739b5-f5cd-48c0-baf6-b905836a1ca4')
        except Exception as e:
            print(e)
        self.__capital = float(data['available'])

    def get_capital(self):
        return int(self.__capital)
