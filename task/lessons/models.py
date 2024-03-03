from django.db import models
from task.products.models import Product


class Lesson(models.Model):
    name = models.CharField(max_length=255, unique=True)
    video = models.URLField(max_length=200, unique=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='lessons',
    )

    def __str__(self):
        return self.name
