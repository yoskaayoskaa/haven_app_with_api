from rest_framework import fields, serializers

from products.models import BasketItem, Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())
    price = fields.FloatField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'quantity', 'image', 'category')


class BasketItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    item_sum = fields.FloatField(required=False)
    total_quantity = fields.SerializerMethodField()
    total_sum = fields.SerializerMethodField()

    class Meta:
        model = BasketItem
        fields = ('id', 'product', 'quantity', 'item_sum', 'total_quantity', 'total_sum', 'created_timestamp')
        read_only_fields = ('created_timestamp',)

    def get_total_quantity(self, obj):
        return BasketItem.objects.filter(user_id=obj.user.id).total_quantity()

    def get_total_sum(self, obj):
        return BasketItem.objects.filter(user_id=obj.user.id).total_sum()
