from open_authenticated import Order

#Verifies that there is a long position by getting
#the last order collected
#There is a long position as long as an order has been filled
#and th eside was buying


class OpenPosition:

    def __init__(self, order=Order()):
        self.open_position = False
        self.order = order

    def get_position(self):
        return self.open_position

    def set_position(self):
        if self.order.status == 'filled' and self.order.side == 'buy':
            self.open_position = True
