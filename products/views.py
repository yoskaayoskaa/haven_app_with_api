from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from general.views import GeneralMixin
from products.models import BasketItem, Product, ProductCategory


class IndexView(GeneralMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'HAVEN - Главная'


class ProductsListView(GeneralMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    title = 'HAVEN - Каталог'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset().order_by('pk')
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


@login_required
def basket_add(request, product_id):
    BasketItem.create_or_update(product_id=product_id, user=request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, basket_item_id):
    basket_item = BasketItem.objects.get(id=basket_item_id)
    basket_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
