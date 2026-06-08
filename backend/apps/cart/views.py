from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from apps.catalog.models import Product
from .cart import Cart


class CartView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cart = Cart(request)
        return Response({
            'items':       list(cart),
            'grand_total': str(cart.grand_total),
            'count':       len(cart),
        })

    def post(self, request):
        """Add item. Body: {product_id, quantity}"""
        try:
            product = Product.objects.get(id=request.data['product_id'], in_stock=True)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found or out of stock.'}, status=404)
        cart = Cart(request)
        cart.add(product, quantity=int(request.data.get('quantity', 1)))
        return Response({'message': 'Added.', 'count': len(cart)})

    def patch(self, request):
        """Update quantity. Body: {product_id, quantity}"""
        cart = Cart(request)
        cart.update(request.data['product_id'], int(request.data['quantity']))
        return Response({'message': 'Updated.', 'count': len(cart)})

    def delete(self, request):
        """Remove item. Body: {product_id}"""
        cart = Cart(request)
        cart.remove(request.data['product_id'])
        return Response({'message': 'Removed.', 'count': len(cart)})


class CartClearView(APIView):
    permission_classes = [permissions.AllowAny]

    def delete(self, request):
        Cart(request).clear()
        return Response({'message': 'Cart cleared.'})