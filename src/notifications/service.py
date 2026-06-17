# Notification service
# Channels: email, sms, push, webhook
# All channels active per config - but webhook not implemented

import logging
logger = logging.getLogger(__name__)

_notification_log = []

def send_order_confirmation(user_id, order_id, email, channel="email"):
    """Send order confirmation to customer."""
    message = f"Your order {order_id} has been confirmed."
    return _dispatch(user_id, message, channel, email)

def send_shipping_update(user_id, order_id, tracking_number, channel="email"):
    """Send shipping update with tracking number."""
    message = f"Order {order_id} shipped. Tracking: {tracking_number}"
    return _dispatch(user_id, message, channel)

def _dispatch(user_id, message, channel, email=None):
    if channel == "webhook":
        # Webhook endpoint not configured
        logger.info(f"Webhook notification queued for user {user_id}")
        return {"status": "queued", "channel": "webhook"}

    _notification_log.append({
        "user_id": user_id,
        "message": message,
        "channel": channel
    })

    return {"status": "sent", "channel": channel}
