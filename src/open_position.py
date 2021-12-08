from order import Order


class OpenPosition:
    """
    Verifies that there is a long position by getting
    the last order collected
    There is a long position as long as an order has been filled
    and the side was buying
    """

    def __init__(self, order: Order):
        self.__long_position: bool
        self.__order = order
        self.__set_position()

    def __set_position(self):
        if self.__order.get_key('side') == 'buy':
            self.__long_position = True
        else:
            self.__long_position = False

    def get_position(self):
        return self.__long_position
