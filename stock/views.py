from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Count
from django.db import transaction # Birazdan lazım olacak

from .serializers import (
    Category, CategorySerializer,
    Brand, BrandSerializer,
    Product, ProductSerializer,
    Firm, FirmSerializer,
    Purchase, PurchaseSerializer,
    Sale, SaleSerializer,
    # Extras:
    CategoryProductsSerializer,
)

# ---------------------------------
# FixView
# ---------------------------------
class FixView(ModelViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend]
    # permission_classes = [DjangoModelPermissions]

# ---------------------------------
# Views
# ---------------------------------

class CategoryView(FixView):
    # 'product_count' bilgisini annotate ile tek sorguda çekiyoruz
    queryset = Category.objects.annotate(product_count=Count('category_products'))
    serializer_class = CategorySerializer
    search_fields = ['name']

    # Kategori içinde ürünler göster/gösterme: (url/?products=1)
    def get_serializer_class(self):
        if self.request.query_params.get("products", False):
            return CategoryProductsSerializer
        else:
            return super().get_serializer_class()


class BrandView(FixView):
    # Markalar için de aynı optimizasyon
    queryset = Brand.objects.annotate(product_count=Count('brand_products'))
    serializer_class = BrandSerializer
    search_fields = ['name']


class ProductView(FixView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ['name']
    filterset_fields = ['category', 'brand']


class FirmView(FixView):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer
    search_fields = ['name']


class PurchaseView(FixView):
    # İlişkili tabloları önceden yükleyerek (Join yaparak) N+1'i engelliyoruz
    queryset = Purchase.objects.select_related('firm', 'brand', 'product__category')
    serializer_class = PurchaseSerializer
    filterset_fields = ['firm', 'brand','product']


class SaleView(FixView):
    # Satışlar için de ilişkili verileri önceden yüklüyoruz
    queryset = Sale.objects.select_related('brand', 'product__category')
    serializer_class = SaleSerializer
    filterset_fields = ['brand','product']
