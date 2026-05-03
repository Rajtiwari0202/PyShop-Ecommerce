from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    stock = models.IntegerField()
    description = models.TextField(blank=True)
    image_url = models.URLField()

    def __str__(self):
        return self.name