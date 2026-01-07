from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    qr_code = models.CharField(max_length=255, unique=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product_name} - {self.qr_code}"
from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

