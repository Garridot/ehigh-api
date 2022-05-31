from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.forms import ValidationError
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email,password=None,**extra_fields):

        if not email: raise ValidationError('User must have an Email.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user  

    def create_superuser(self, email,password):

        user = self.create_user(email,password)
        user.is_staff     = True
        user.is_superuser = True
        user.save(using=self._db)   

        return user 


class User(AbstractBaseUser,PermissionsMixin):
    email     = models.EmailField(max_length=100,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email' 


status_choice   = (('stock','Stock'),('out-of-stock','Out-of-stock')) 
class Product(models.Model):
    name   = models.CharField(max_length=100)
    price  = models.FloatField()
    stock  = models.IntegerField()     
    status = models.CharField(max_length=100, default='stock', choices=status_choice,)  

    def __str__(self):
        return self.name

class Order(models.Model):
    date_time  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"  

    @property
    def get_total(self):
        details = self.orderdetail_set.all()
        total   = sum([item.get_total_product for item in details])
        return  total  

    # @property
    # def get_total_usd(self):   
       
    #     return self.get_total * dolar_blue 
 


class OrderDetail(models.Model): 

    order    = models.ForeignKey(Order,on_delete=models.CASCADE)  
    cuantity = models.IntegerField()
    product  = models.ForeignKey(Product,on_delete=models.CASCADE) 

    @property
    def get_total_product(self):        
        total = self.product.price * self.cuantity
        return total 
