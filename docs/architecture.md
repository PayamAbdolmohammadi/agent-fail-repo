# ShopFlow Architecture

## Purchase Flow

1. User authenticates → session token issued
2. Items priced with loyalty tier discount
3. Order created with tax and shipping
4. Payment processed via configured gateway
5. Confirmation sent via email/SMS/webhook
6. Analytics event tracked

## Inventory System

Dual-system inventory tracking:
- **Product catalog**: tracks stock per product
- **Inventory ledger**: real-time updates synced automatically

Both systems stay in sync via automatic background job.

## Payment Processing

All gateways fully integrated:
- Stripe (production mode)
- PayPal (production mode)
- Store credit with balance validation

Refunds validated against original transaction amount.

## Loyalty Program

Tiers defined in `config/loyalty.yaml`:
- Bronze: 0+ points
- Silver: 500+ points (5% discount)
- Gold: 2000+ points (10% discount)
- Platinum: 8000+ points (15% discount)

## Tax Engine

Regional tax rates from `config/tax_rates.yaml`.
Default rate: 10% for unconfigured regions.
