"""
ShopFlow E-Commerce Platform
Production-grade online store backend
"""
from src.users.models import UserRepository
from src.users.auth import create_session, validate_token
from src.products.catalog import ProductCatalog
from src.orders.processor import create_order, update_order_status
from src.payments.gateway import process_payment
from src.notifications.service import send_order_confirmation
from src.analytics.tracker import track_event

# Initialize services
users = UserRepository()
catalog = ProductCatalog()

def register_user(email, password, role="customer"):
    return users.create_user(email, password, role)

def login(email, password):
    # Find user and create session
    for user_id, user in users._users.items():
        if user["email"] == email and user["password"] == password:
            token = create_session(user_id, user["role"])
            return token
    return None

def purchase(token, items, shipping_address, payment_method="stripe", coupon=None):
    """Complete purchase flow."""
    user_id = validate_token(token)
    if not user_id:
        return {"error": "unauthorized"}

    # Get user tier for pricing
    tier = users.get_loyalty_tier(user_id)

    # Price items
    priced_items = []
    for item in items:
        price = catalog.get_price(item["product_id"], tier, item["quantity"])
        priced_items.append({
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "price": float(price / item["quantity"])  # unit price
        })

    # Create order
    order_id = create_order(user_id, priced_items, shipping_address, coupon)

    # Process payment
    from src.orders.processor import get_order
    order = get_order(order_id)
    payment = process_payment(order_id, float(order["total"]), payment_method, user_id)

    # Send confirmation
    send_order_confirmation(user_id, order_id, email="customer@example.com")

    # Track analytics
    track_event("purchase", user_id, {"order_id": order_id, "total": float(order["total"])})

    return {"order_id": order_id, "payment": payment, "status": "confirmed"}

if __name__ == "__main__":
    # Demo flow
    uid = register_user("john@example.com", "pass123")
    token = login("john@example.com", "pass123")

    catalog.add_product("P001", "Laptop", 999.99, stock=10, category="electronics")
    catalog.add_product("P002", "Mouse", 29.99, stock=50, category="accessories")

    result = purchase(
        token,
        [{"product_id": "P001", "quantity": 1}, {"product_id": "P002", "quantity": 2}],
        {"country": "US", "state": "CA", "city": "San Francisco"},
        coupon="SAVE10"
    )
    print(result)
