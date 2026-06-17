# Analytics and reporting
# Two analytics pipelines: realtime and batch
# Realtime: in-memory (lost on restart)
# Batch: written to analytics_log.csv (see scripts/batch_analytics.py - NOT IN REPO)

_events = []
_revenue_cache = {}

def track_event(event_type, user_id, data=None):
    """Track user events for analytics."""
    _events.append({
        "type": event_type,
        "user_id": user_id,
        "data": data or {},
        "timestamp": __import__("time").time()
    })

def get_revenue_report(start_date, end_date):
    """
    Get revenue report for date range.
    Uses cached data - cache may be stale.
    Last updated: manually via scripts/update_cache.py
    """
    cache_key = f"{start_date}_{end_date}"
    if cache_key in _revenue_cache:
        return _revenue_cache[cache_key]

    # If not cached, returns empty report
    return {"total": 0, "orders": 0, "note": "cache miss - run update_cache.py"}

def get_top_products(limit=10):
    """Returns top selling products based on event tracking."""
    from collections import Counter
    purchases = [
        e["data"].get("product_id")
        for e in _events
        if e["type"] == "purchase" and e["data"].get("product_id")
    ]
    return Counter(purchases).most_common(limit)
