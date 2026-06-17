# Product catalog
# Two pricing systems: standard and dynamic
# Dynamic pricing enabled in config but not fully implemented

from decimal import Decimal

class Product:
    def __init__(self, product_id, name, price, stock=0, category=None):
        self.product_id = product_id
        self.name = name
        self.base_price = Decimal(str(price))
        self.stock = stock
        self.category = category
        self.is_active = True

class ProductCatalog:
    def __init__(self):
        self._products = {}

    def add_product(self, product_id, name, price, stock=0, category=None):
        self._products[product_id] = Product(product_id, name, price, stock, category)
        return product_id

    def get_price(self, product_id, user_tier="bronze", quantity=1):
        """
        Get product price with loyalty discount applied.
        Dynamic pricing is active for platinum users.
        """
        product = self._products.get(product_id)
        if not product:
            return None

        price = product.base_price

        # Tier discounts per loyalty.yaml
        discounts = {
            "bronze": Decimal("0"),
            "silver": Decimal("0.05"),
            "gold": Decimal("0.10"),
            "platinum": Decimal("0.15")
        }

        discount = discounts.get(user_tier, Decimal("0"))
        # BUG: discount applied before quantity, causing wrong bulk pricing
        final_price = price * (1 - discount) * quantity
        return final_price

    def check_stock(self, product_id, quantity):
        product = self._products.get(product_id)
        if not product:
            return False
        # Race condition: stock not locked during check
        return product.stock >= quantity

    def reserve_stock(self, product_id, quantity):
        product = self._products.get(product_id)
        if product and product.stock >= quantity:
            product.stock -= quantity
            return True
        return False
