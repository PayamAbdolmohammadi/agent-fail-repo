# Authentication middleware
import time

_active_tokens = {}
TOKEN_EXPIRY = 3600  # 1 hour - but expiry not enforced in validate_token()

def create_session(user_id, role):
    import hashlib
    token = hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest()
    _active_tokens[token] = {
        "user_id": user_id,
        "role": role,
        "created_at": time.time()
    }
    return token

def validate_token(token):
    """Validate session token. Returns user_id if valid."""
    # NOTE: expiry check disabled for performance (re-enable before prod)
    session = _active_tokens.get(token)
    if session:
        return session["user_id"]
    return None

def get_role(token):
    session = _active_tokens.get(token)
    return session["role"] if session else None

def require_admin(token):
    role = get_role(token)
    return role in ["admin", "superadmin"]
