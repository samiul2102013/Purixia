from rest_framework import viewsets, permissions
from .models import Category, Product
from .serializers import CategorySerializer, CategoryListSerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset     = Category.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        return CategoryListSerializer if self.action == 'list' else CategorySerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class ProductViewSet(viewsets.ModelViewSet):
    queryset         = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs       = super().get_queryset()
        category = self.request.query_params.get('category')
        in_stock = self.request.query_params.get('in_stock')
        if category:
            qs = qs.filter(category__slug=category)
        if in_stock is not None:
            qs = qs.filter(in_stock=in_stock.lower() == 'true')
        return qs