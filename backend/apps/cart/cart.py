from decimal import Decimal
from apps.catalog.models import Product

CART_SESSION_KEY = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def _save(self):
        self.session[CART_SESSION_KEY] = self.cart
        self.session.modified = True

    def add(self, product, quantity=1):
        pid = str(product.id)
        if pid not in self.cart:
            self.cart[pid] = {'quantity': 0, 'price': str(product.price)}
        self.cart[pid]['quantity'] += quantity
        self._save()

    def remove(self, product_id):
        self.cart.pop(str(product_id), None)
        self._save()

    def update(self, product_id, quantity):
        pid = str(product_id)
        if pid in self.cart:
            if quantity <= 0:
                self.remove(product_id)
            else:
                self.cart[pid]['quantity'] = quantity
                self._save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.session.modified = True

    def __iter__(self):
        ids      = self.cart.keys()
        products = Product.objects.filter(id__in=ids)
        cart     = dict(self.cart)
        for product in products:
            entry = cart[str(product.id)]
            entry['product'] = {
                'id':    product.id,
                'name':  product.name,
                'price': str(product.price),
                'image': product.image.url if product.image else None,
            }
            entry['total_price'] = str(Decimal(entry['price']) * entry['quantity'])
            yield entry

    @property
    def grand_total(self):
        return sum(Decimal(v['price']) * v['quantity'] for v in self.cart.values())

    def __len__(self):
        return sum(v['quantity'] for v in self.cart.values())