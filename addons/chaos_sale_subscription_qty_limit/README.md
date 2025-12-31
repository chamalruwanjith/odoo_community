# Sale Subscription Quantity Limit

## Overview

This module prevents customers from adding more than 1 quantity of specific subscription upsell products in the customer portal.

## Features

- ✅ **Automatic Detection**: Identifies products with specific `trazet_product_key` values
- ✅ **Quantity Limit**: Enforces maximum quantity of 1 for targeted products
- ✅ **UI Feedback**: Disables (+) button when quantity reaches limit
- ✅ **Input Validation**: Prevents manual quantity input above limit
- ✅ **User Notifications**: Shows warning message when limit is reached

## Targeted Products

The module limits quantity to 1 for products with these `trazet_product_key` values:
- `allowExternalAPI`
- `collectPeriod`

## How It Works

### Frontend (Portal)
- Adds `data-product-key` attribute to order lines in subscription portal
- JavaScript intercepts quantity changes
- Enforces maximum quantity of 1
- Disables (+) button when limit reached
- Shows warning notification if user tries to exceed limit

### Template Inheritance
- Extends `sale.sale_order_portal_content` template
- Adds data attributes to order line rows for JavaScript detection

## Installation

1. Copy module to your Odoo addons directory
2. Update Apps list
3. Install "Sale Subscription Quantity Limit"

## Configuration

No configuration needed - works automatically for products with specified `trazet_product_key` values.

## Technical Details

**Module Name**: `chaos_sale_subscription_qty_limit`
**Version**: 18.0.1.0.0
**Depends on**: `sale_subscription`, `portal`
**License**: OPL-1

### Template Inheritance
- `sale.sale_order_portal_content` - Added data attributes for product detection

### JavaScript
- Pure JavaScript implementation (no jQuery dependency)
- Uses MutationObserver for dynamic content updates
- Intercepts quantity buttons and input changes

## Use Cases

- Limit subscription add-on products to 1 per order
- Restrict API access products to single quantity
- Control ordering of specific upsell items

## Author

**ChaosHub**
Website: https://chaoshub.lk/

## License

OPL-1 (Odoo Proprietary License v1.0)
