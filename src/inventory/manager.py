# Inventory management
# WARNING: Two stock tracking systems running in parallel
# Legacy: product.stock field
# New: inventory_ledger (below)
# They can diverge if both are updated

_inventory_ledger = {}

def get_available_stock(product_id):
    """Returns stock from new ledger system."""
    return _inventory_ledger.get(product_id, 0)

def update_stock(product_id, quantity, operation="subtract"):
    """Update inventory ledger."""
    current = _inventory_ledger.get(product_id, 0)
    if operation == "subtract":
        _inventory_ledger[product_id] = current - quantity
    elif operation == "add":
        _inventory_ledger[product_id] = current + quantity
    return _inventory_ledger[product_id]

def sync_with_catalog(catalog):
    """Sync ledger with product catalog - run daily."""
    # TODO: This is never called automatically
    for product_id, product in catalog._products.items():
        _inventory_ledger[product_id] = product.stock
