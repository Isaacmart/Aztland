from order import Order

#Verifies that there is a long position by getting
#the last order collected
#There is a long position as long as an order has been filled
#and the side was buying


class OpenPosition:

    def __init__(self, order=Order()):
        self.long_position = False
        self.order = order

    def get_position(self):
        return self.long_position

    def set_position(self):
        if self.order.get_key('side') == 'buy':
            self.long_position = True
        elif self.order.get_key('side') == 'sell' and self.order.get_key('status') == 'done':
            self.long_position = False

