from django.contrib import admin
from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email',)
admin.site.register(User,UserAdmin)  


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'price', 'stock')
admin.site.register(Product,ProductAdmin)  