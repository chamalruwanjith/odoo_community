# Website Sale Quantity Limit for Upsell

## Overview

This module prevents customers from adding more than 1 quantity of upsell/optional products in the shopping cart.

## Features

- ✅ **Automatic Detection**: Identifies optional/upsell products (products with `linked_line_id`)
- ✅ **Quantity Limit**: Enforces maximum quantity of 1 for upsell products
- ✅ **UI Feedback**: Disables (+) button when quantity reaches limit
- ✅ **Input Validation**: Prevents manual quantity input above limit
- ✅ **User Notifications**: Shows warning message when limit is reached

## What are Upsell/Optional Products?

In Odoo, optional products are:
- Products suggested during checkout
- Products linked to main order lines via `linked_line_id`
- Cross-sell or up-sell products shown in the cart

## How It Works

### Backend
- Adds `_is_upsell_line()` method to `sale.order.line` model
- Checks if line has a `linked_line_id` (indicates optional product)

### Frontend
- Adds `data-is-upsell` and `data-max-qty` attributes to cart lines
- JavaScript intercepts quantity changes
- Enforces maximum quantity of 1
- Disables (+) button when limit reached
- Shows warning notification if user tries to exceed limit

## Installation

1. Copy module to your Odoo addons directory
2. Update Apps list
3. Install "Website Sale Quantity Limit for Upsell"

## Configuration

No configuration needed - works automatically for all optional products.

## Technical Details

**Module Name**: `chaos_website_sale_qty_limit`
**Version**: 18.0.1.0.0
**Depends on**: `website_sale`
**License**: OPL-1

### Modified Models
- `sale.order.line` - Added `_is_upsell_line()` method

### Template Inheritance
- `website_sale.cart_lines` - Added data attributes for upsell detection

### JavaScript Extensions
- Extends `WebsiteSale` widget
- Overrides `_changeCartQuantity()` and `_onChangeCartQuantity()`

## Use Cases

- Limit promotional items to 1 per order
- Restrict free gifts to single quantity
- Prevent bulk ordering of add-on products
- Control inventory for limited optional items

## Author

**ChaosHub**
Website: https://chaoshub.lk/

## License

OPL-1 (Odoo Proprietary License v1.0)
