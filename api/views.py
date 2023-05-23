from rest_framework import status
from rest_framework.permissions import (SAFE_METHODS, IsAdminUser,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.models import BasketItem, Product
from products.serializers import BasketItemSerializer, ProductSerializer


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = (IsAdminUser,)

        return super(ProductModelViewSet, self).get_permissions()


class BasketItemModelViewSet(ModelViewSet):
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        queryset = super(BasketItemModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):  # POST
        try:
            product_id = request.data['product_id']
            products = Product.objects.filter(id=product_id)

            if not products.exists():
                return Response(
                    {'status': 'not ok', 'data': 'There is no product with such ID in database'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            obj, is_created = BasketItem.create_or_update(product_id=product_id, user=request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status_code)

        except KeyError:
            return Response(
                {'status': 'not ok', 'product_id': 'This field is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
