from decimal import Decimal
from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.cart import Cart
from apps.catalog.models import Product
from .models import Order, OrderItem, ShippingInfo
from .serializers import OrderSerializer, PlaceOrderSerializer


class PlaceOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def _process_items(self, order, items):
        total = Decimal('0')
        for entry in items:
            product_id = entry.get('product_id') or entry.get('product', {}).get('id')
            if not product_id:
                continue
            try:
                product = Product.objects.select_for_update().get(id=product_id)
            except Product.DoesNotExist:
                raise ValueError(f"Product with ID {product_id} no longer exists.")

            qty = entry['quantity']
            if product.quantity < qty:
                raise ValueError(
                    f"Not enough stock for {product.name}. Available: {product.quantity}, Requested: {qty}"
                )

            price = Decimal(entry.get('price', '0'))
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
                unit_price=price,
            )
            product.quantity -= qty
            if product.quantity <= 0:
                product.in_stock = False
            product.save()
            total += price * qty
        order.total_amount = total
        order.save()

    @transaction.atomic
    def post(self, request):
        cart = Cart(request)

        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        body_items = data.get('items')
        if body_items is not None and len(body_items) > 0:
            items_source = body_items
        elif cart and len(cart) > 0:
            items_source = cart
        else:
            return Response({'error': 'Your cart is empty. Please add items before checkout.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            shipping = ShippingInfo.objects.create(**data['shipping_info'])
            order = Order.objects.create(
                user=request.user,
                shipping_info=shipping,
                delivery_type=data['delivery_type'],
                payment_method=data['payment_method'],
            )
            self._process_items(order, items_source)
            cart.clear()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f"Order placement failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderListView(generics.ListAPIView):
    serializer_class   = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class   = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)