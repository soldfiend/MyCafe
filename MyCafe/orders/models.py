from django.db import models
from menu.models import Dish  # Импорт модели Dish из приложения menu
from users.models import CustomUser

# Определение статусов заказа
ORDER_STATUS_CHOICES = [
    ('не готов', 'Не готов'),
    ('готово', 'Готово'),
    ('в пути', 'В пути'),
    # Добавьте другие статусы, если необходимо
]


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True)

    def total_price(self):
        return self.dish.price * self.quantity


class OrderedItem(models.Model):
    order = models.ForeignKey('Order', related_name='ordered_items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, related_name='orders')
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='не готов')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
