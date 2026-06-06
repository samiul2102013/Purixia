from django.urls import path
from .views import CartView, CartClearView

urlpatterns = [
    path('',       CartView.as_view(),      name='cart'),
    path('clear/', CartClearView.as_view(), name='cart-clear'),
]