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

    @transaction.atomic
    def post(self, request):
        cart = Cart(request)
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"PLACE_ORDER: user={request.user}, auth={request.auth}, session_key={request.session.session_key}, cart_len={len(cart)}, cart_items={dict(cart.cart) if hasattr(cart, 'cart') else 'N/A'}")
        if not cart or len(cart) == 0:
            logger.warning(f"PLACE_ORDER_FAIL: cart empty. session_key={request.session.session_key}, cart_in_session={'cart' in request.session}")
            return Response({'error': 'Your cart is empty. Please add items before checkout.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            # Create shipping info
            shipping = ShippingInfo.objects.create(**data['shipping_info'])
            
            # Create order
            order = Order.objects.create(
                user           = request.user,
                shipping_info  = shipping,
                delivery_type  = data['delivery_type'],
                payment_method = data['payment_method'],
            )

            total = Decimal('0')
            for entry in cart:
                # The entry yielded by Cart.__iter__ has a 'product' dict with an 'id'
                product_id = entry.get('product', {}).get('id')
                if not product_id:
                    continue

                try:
                    product = Product.objects.select_for_update().get(id=product_id)
                except Product.DoesNotExist:
                    return Response({'error': f"Product with ID {product_id} no longer exists."}, status=400)

                qty = entry['quantity']
                if product.quantity < qty:
                    return Response({
                        'error': f"Not enough stock for {product.name}. Available: {product.quantity}, Requested: {qty}"
                    }, status=status.HTTP_400_BAD_REQUEST)

                price = Decimal(entry['price'])
                OrderItem.objects.create(
                    order=order, 
                    product=product, 
                    quantity=qty, 
                    unit_price=price
                )
                
                product.quantity -= qty
                if product.quantity <= 0:
                    product.in_stock = False
                product.save()
                total += price * qty

            order.total_amount = total
            order.save()
            cart.clear()

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
            
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