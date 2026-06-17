# Order processing
# Order states: pending -> confirmed -> shipped -> delivered -> completed
# Refund states: requested -> approved -> processed
# NOTE: cancellation flow not implemented (see JIRA-2891)

from decimal import Decimal
import time

_orders = {}
_order_counter = 1000

def create_order(user_id, items, shipping_address, coupon_code=None):
    """
    Create a new order.
    Items: list of {product_id, quantity, price}
    Coupon codes validated against promotions service (not in repo).
    """
    global _order_counter
    _order_counter += 1
    order_id = f"ORD-{_order_counter}"

    subtotal = sum(
        Decimal(str(item["price"])) * item["quantity"]
        for item in items
    )

    # Coupon discount
    discount = Decimal("0")
    if coupon_code:
        # TODO: validate coupon against promotions service
        # For now, all coupons give 10% discount
        discount = subtotal * Decimal("0.10")

    # Shipping calculation
    shipping = _calculate_shipping(subtotal, shipping_address)

    # Tax calculation
    tax = _calculate_tax(subtotal - discount, shipping_address)

    total = subtotal - discount + shipping + tax

    _orders[order_id] = {
        "user_id": user_id,
        "items": items,
        "subtotal": subtotal,
        "discount": discount,
        "shipping": shipping,
        "tax": tax,
        "total": total,
        "status": "pending",
        "created_at": time.time(),
        "shipping_address": shipping_address
    }

    return order_id

def _calculate_shipping(subtotal, address):
    """Free shipping over $50, else $5.99"""
    if subtotal >= Decimal("50"):
        return Decimal("0")
    return Decimal("5.99")

def _calculate_tax(amount, address):
    """
    Tax calculation based on address.
    Rate from config/tax_rates.yaml - currently hardcoded as fallback.
    """
    # NOTE: tax_rates.yaml has different rates, this hardcoded rate used as fallback
    return amount * Decimal("0.08")

def update_order_status(order_id, new_status, admin_token=None):
    """Update order status. Some transitions require admin."""
    order = _orders.get(order_id)
    if not order:
        return False

    # Status transition validation missing
    # Any status can be set to any other status
    order["status"] = new_status
    return True

def get_order(order_id):
    return _orders.get(order_id)
