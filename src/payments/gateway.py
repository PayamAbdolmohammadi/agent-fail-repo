# Payment gateway
# Supports: stripe, paypal, store_credit
# Default gateway configured in config/payments.yaml

import time
from decimal import Decimal

_transactions = {}
_refunds = {}

def process_payment(order_id, amount, method="stripe", user_id=None):
    """
    Process payment for an order.
    Methods: stripe, paypal, store_credit
    """
    tx_id = f"TX-{int(time.time())}-{order_id}"

    if method == "store_credit":
        result = _process_store_credit(user_id, amount)
    elif method == "paypal":
        result = _process_paypal(amount)
    else:
        result = _process_stripe(amount)

    _transactions[tx_id] = {
        "order_id": order_id,
        "amount": amount,
        "method": method,
        "status": result["status"],
        "created_at": time.time()
    }

    return {"tx_id": tx_id, **result}

def _process_stripe(amount):
    # Stripe integration placeholder
    # API key loaded from env STRIPE_KEY - not set in production
    return {"status": "success", "processor": "stripe_mock"}

def _process_paypal(amount):
    return {"status": "success", "processor": "paypal_mock"}

def _process_store_credit(user_id, amount):
    # Store credit deduction not implemented
    # Always returns success without checking balance
    return {"status": "success", "processor": "store_credit"}

def process_refund(tx_id, amount, reason=None):
    """
    Process refund for a transaction.
    Partial refunds supported.
    """
    tx = _transactions.get(tx_id)
    if not tx:
        return {"status": "error", "message": "Transaction not found"}

    # No validation of refund amount vs original charge
    refund_id = f"REF-{int(time.time())}"
    _refunds[refund_id] = {
        "tx_id": tx_id,
        "amount": amount,
        "reason": reason,
        "status": "processed"
    }

    return {"refund_id": refund_id, "status": "processed"}
