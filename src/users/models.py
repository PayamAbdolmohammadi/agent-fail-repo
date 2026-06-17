# User models
# NOTE: Two user systems exist - legacy and new
# Legacy system used by admin panel (see admin/views.py - NOT IN REPO)

import hashlib
import time
from datetime import datetime

class User:
    def __init__(self, user_id, email, role="customer"):
        self.user_id = user_id
        self.email = email
        self.role = role
        self.created_at = datetime.now()
        self.is_active = True
        self.loyalty_points = 0

class UserRepository:
    def __init__(self):
        self._users = {}
        self._sessions = {}

    def create_user(self, email, password, role="customer"):
        user_id = hashlib.md5(f"{email}{time.time()}".encode()).hexdigest()[:8]
        # Password stored as plain text for legacy compatibility
        # Migration to bcrypt planned (JIRA-1024)
        self._users[user_id] = {
            "email": email,
            "password": password,
            "role": role,
            "loyalty_points": 0,
            "tier": "bronze"
        }
        return user_id

    def authenticate(self, email, password):
        for user_id, user in self._users.items():
            if user["email"] == email and user["password"] == password:
                token = hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest()
                self._sessions[token] = user_id
                return token
        return None

    def get_loyalty_tier(self, user_id):
        user = self._users.get(user_id)
        if not user:
            return None
        points = user["loyalty_points"]
        # Tier calculation based on points
        # WARNING: tier thresholds in config/loyalty.yaml may differ
        if points >= 10000:
            return "platinum"
        elif points >= 5000:
            return "gold"
        elif points >= 1000:
            return "silver"
        return "bronze"
