import uuid
from django.db import models


class PizzaOrderModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=50, unique=False, null=False, default='new')
    customer_name = models.TextField(null=False, blank=False)
    customer_email = models.EmailField(null=True)
    customer_mobile = models.CharField(max_length=30, unique=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return 'The order with Identifier {} for customer : {}, create at {}; The Status is {} ' \
            .format(self.id, self.customer_name, self.created_at, self.status)

    class Meta:
        db_table = "pizza_orders"
        ordering = ['-created_at']


class PizzaOrderItemsModel(models.Model):

    pizza_flavour = models.CharField(max_length=30, null=False)
    pizza_size = models.CharField(max_length=10, null=False, default='medium')
    pizza_count = models.IntegerField(null=False, default=1)
    item_number = models.IntegerField(null=False, default=1)
    pizza_order = models.ForeignKey(PizzaOrderModel, on_delete=models.PROTECT, related_name = 'pizza_order_id')

    def __str__(self) -> str:
        return 'Item Number : {}, Flavour : {}, Size : {}, Count : {}'.format(
            self.item_number, self.pizza_flavour, self.pizza_size, self.pizza_count)

    class Meta:
        db_table = "pizza_order_items"
        ordering = ["item_number"]