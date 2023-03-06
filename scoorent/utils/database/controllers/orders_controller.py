from ..model import Connector


class OrdersController(Connector):
    """`Orders` table controller."""

    def create_order(self):
        """Create order."""


orders_controller = OrdersController()
