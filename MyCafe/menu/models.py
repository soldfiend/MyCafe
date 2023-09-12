from django.db import models


# Create your models here.

CATEGORY_CHOICES = (
    ('breakfast', 'Завтрак'),
    ('lunch', 'Обед'),
    ('dinner', 'Ужин'),
)


class Dish(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image_url = models.URLField(verbose_name='Фото')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, verbose_name='Категория')

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def __str__(self):
        return self.name


