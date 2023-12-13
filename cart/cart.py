from django.conf import settings
from product.models import Product
import json

# @login_required
class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            product_id = str(product.id)
            self.cart[product_id]['product'] = product

        for item in self.cart.values():
            item['total_price'] = int(item['product'].price * item['quantity'])
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product_id, quantity=1, update_quantity = False):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'id': product_id}

        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)
            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
        self.save()

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_item_price(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)
        price = sum(item['product'].price * item['quantity'] for item in self.cart.values())
        return price

    def get_total_price(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)
        price = sum(item['product'].price * item['quantity'] for item in self.cart.values())
        if price < 500:
            return int(price + 250)
        else:
            return price

    def get_item(self, product_id):
        if str(product_id) in self.cart:
            return self.cart[str(product_id)]
        else:
            None

    def to_json(self):
        # Convert the cart object to a dictionary
        cart_dict = {
            'cart': list(self.cart.values()),
            'total_item_price': self.get_total_item_price(),
            'total_price': self.get_total_price(),
        }

        # Serialize the dictionary to JSON using the custom encoder
        cart_json = json.dumps(cart_dict, cls=CartEncoder)
        return cart_json