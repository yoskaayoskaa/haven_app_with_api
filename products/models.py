import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def is_active(self):
        products_in_category = Product.objects.filter(category=self)
        if products_in_category.exists():
            return True

        return False


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=0)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images', blank=True, null=True)
    stripe_product_price_id = models.CharField(max_length=128, blank=True, null=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f'<Продукт: {self.name} | Категория: {self.category.name}>'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency='rub',
        )
        return stripe_product_price


class BasketItemQuerySet(models.QuerySet):
    def total_quantity(self):
        return sum(basket_item.quantity for basket_item in self)

    def total_sum(self):
        return sum(basket_item.item_sum() for basket_item in self)

    def stripe_line_items(self):
        return [
            {'price': basket_item.product.stripe_product_price_id, 'quantity': basket_item.quantity}
            for basket_item in self
        ]


class BasketItem(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketItemQuerySet.as_manager()

    def __str__(self):
        return f'Позиция для {self.user.username} | Продукт {self.product.name} | Количество {self.quantity}'

    def item_sum(self):
        return self.product.price * self.quantity

    def decode_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.item_sum()),
        }
        return basket_item

    @staticmethod
    def create_or_update(product_id, user):
        basket_item = BasketItem.objects.filter(user=user, product_id=product_id).first()

        if not basket_item:
            new_basket_item = BasketItem.objects.create(user=user, product_id=product_id, quantity=1)
            is_created = True
            return new_basket_item, is_created
        else:
            basket_item.quantity += 1
            basket_item.save()
            is_created = False
            return basket_item, is_created
