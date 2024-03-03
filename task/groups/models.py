from django.db import models
from task.users.models import CustomUser
from task.products.models import Product


class Group(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='groups')
    users = models.ManyToManyField(CustomUser, blank=True)

    def __str__(self):
        return self.name
