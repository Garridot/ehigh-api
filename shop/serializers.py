from rest_framework import serializers
from rest_framework import status
from core.models import *


def is_lower(value):
    if value < 1:
        raise serializers.ValidationError('Value cannot be lower than 1.',code=status.HTTP_400_BAD_REQUEST)      

def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required',code=status.HTTP_400_BAD_REQUEST)      



class ProductSerializer(serializers.ModelSerializer): 
    name   = serializers.CharField(validators=[required])
    price  = serializers.FloatField(validators=[required,is_lower])
    stock  = serializers.IntegerField(validators=[required,is_lower])     

    class Meta:
        model  = Product
        fields =  ('__all__')

    def validate(self, attrs):                   
        return super().validate(attrs) 

class OrderSerializer(serializers.ModelSerializer):    

    # date_time     = serializers.ReadOnlyField(format="%Y-%m-%dT%H:%M:%S") 
    get_total     = serializers.ReadOnlyField()
    get_total_usd = serializers.ReadOnlyField()

    class Meta:
        model  = Order        
        fields =  ('id','date_time','get_total','get_total_usd')
       
      

class OrderDetailSerializer(serializers.ModelSerializer):

    cuantity = serializers.IntegerField(validators=[required,is_lower])

    class Meta:
        model  = OrderDetail       
        fields =  ('__all__')


    def validate(self, attrs):

        order    = attrs['order']
        product  = attrs['product']
        cuantity = attrs['cuantity'] 
        
        if OrderDetail.objects.filter(order=order,product=product).exists():
            data   = {'Message':'Ya se solicito este producto en la orden.'}
            raise serializers.ValidationError(data)


        get_prod  = Product.objects.get(name=product)     

        if get_prod.status == 'out-of-stock': 
            data   = {'Message':'This product is out-of-stock.'}
            raise serializers.ValidationError(data)     

        if get_prod.stock < cuantity: 
            data   = {'Message':f'No stock available. Stock available: {get_prod.stock}'}
            raise serializers.ValidationError(data) 



        return super().validate(attrs)

      

    

      