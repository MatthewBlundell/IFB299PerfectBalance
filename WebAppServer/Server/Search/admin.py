from django.contrib import admin
from .models import User, Order, Vehicle, Store

#Register your models here.
admin.site.register(User)
admin.site.register(Order)
admin.site.register(Vehicle)
admin.site.register(Store)