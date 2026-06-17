from src.orders.processor import create_order, get_order
from src.products.catalog import ProductCatalog

def test_order_creation():
    items = [{"product_id": "P001", "quantity": 2, "price": 29.99}]
    order_id = create_order("user123", items, {"country": "US", "state": "CA"})
    assert order_id.startswith("ORD-")

def test_order_total():
    items = [{"product_id": "P001", "quantity": 1, "price": 100.00}]
    order_id = create_order("user123", items, {"country": "US", "state": "NY"})
    order = get_order(order_id)
    assert order["total"] > 0

def test_free_shipping():
    items = [{"product_id": "P001", "quantity": 1, "price": 60.00}]
    order_id = create_order("user123", items, {"country": "US"})
    order = get_order(order_id)
    assert order["shipping"] == 0
