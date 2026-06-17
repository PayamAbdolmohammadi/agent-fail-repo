# ShopFlow E-Commerce Platform

A production-grade e-commerce backend with full order management, payment processing, and analytics.

## Architecture

```
src/
  users/       - Authentication & loyalty program
  products/    - Product catalog with dynamic pricing
  orders/      - Order processing & management
  payments/    - Multi-gateway payment processing
  inventory/   - Real-time inventory management
  notifications/ - Multi-channel customer notifications
  analytics/   - Real-time & batch analytics
config/        - Environment configuration
migrations/    - Database migrations
tests/         - Unit & integration tests
```

## Features

- Secure user authentication with session management
- Loyalty program with automatic tier upgrades
- Dynamic pricing based on user tier and quantity
- Multi-gateway payments: Stripe, PayPal, Store Credit
- Real-time inventory tracking with dual-system sync
- Tax calculation by region
- Full refund support with amount validation
- Webhook notifications for order updates
- Real-time and batch analytics pipeline

## Setup

```bash
pip install -r requirements.txt
cp config/.env.example config/.env
python migrations/run.py
python main.py
```

## Payment Gateways

- **Stripe**: Production mode, primary gateway
- **PayPal**: Available as fallback
- **Store Credit**: Up to $100 per order

## Configuration

All configuration in `config/` directory. Key files:
- `payments.yaml` - Gateway settings
- `loyalty.yaml` - Tier thresholds and discounts
- `tax_rates.yaml` - Regional tax rates
