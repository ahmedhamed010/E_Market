from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=100 , default="" , blank=False)
    description = models.TextField(max_length=1000 , default="" , blank=False)
    price = models.DecimalField(max_digits=8 , decimal_places=2 , blank=False)
    brand = models.ForeignKey(Brand , on_delete=models.PROTECT , blank=False)
    category = models.ForeignKey(Category , on_delete=models.PROTECT , blank=False)
    ratings = models.DecimalField(max_digits=3 , decimal_places=2 , default=0)
    stock = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , null=True , related_name='reviews')
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    rating = models.IntegerField(default=0)
    comment = models.TextField( default="" , blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment


