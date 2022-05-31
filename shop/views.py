from rest_framework.viewsets import ModelViewSet
from .serializers import *
from core.models import Product
from rest_framework.response import Response
from .utils import *
# Create your views here.

class ProductView(ModelViewSet):
    
    serializer_class   = ProductSerializer
    queryset           = Product.objects.all()

    def list(self, request):

        queryset   = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class OrderView(ModelViewSet):   

    serializer_class   = OrderSerializer
    queryset           = Order.objects.all()

    def list(self, request):

        queryset   = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        data = self.get_object()
        
        actions = OrderActions(data)
        actions.return_stock()
        return super().destroy(request, *args, **kwargs)    



class OrderDetailView(ModelViewSet):

    serializer_class   = OrderDetailSerializer
    queryset           = OrderDetail.objects.all()

    def list(self, request):

        queryset   = OrderDetail.objects.all()
        serializer = OrderDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, validated_data):
        data = validated_data.data         

        action = OrderDetailActions(data['product'],data['order'],data['cuantity']) 
        action.get_stock()        

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
    
        return Response(serializer.data, status=status.HTTP_201_CREATED, ) 

    def destroy(self, request, *args, **kwargs):
        data = self.get_object()

        action = OrderDetailActions(data.product.id,data.order,data.cuantity) 
        action.return_stock()

        return super().destroy(request, *args, **kwargs)    
            

    