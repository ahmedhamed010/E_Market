from django.contrib import admin
from .models import *  #<= all
# Register your models here.

admin.site.register(Order)
admin.site.register(OrderItem)
