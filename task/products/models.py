from django.db import models
from task.users.models import CustomUser


# Create your models here.
class Product(models.Model):
    name = models.CharField(unique=True, max_length=255)
    start_date = models.DateTimeField(auto_now_add=False)
    price = models.IntegerField()
    min_users = models.IntegerField()
    max_users = models.IntegerField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='author'
    )

    def __str__(self):
        return self.name

    def is_bought(self, user):
        return True if user in self.groups else False
