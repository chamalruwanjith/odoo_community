# POS Hide Taxes

## Overview

This module customizes the Point of Sale receipt to hide tax-related information, providing a cleaner receipt format.

## Features

- **Hides untaxed amount**: The subtotal without taxes is not displayed
- **Hides tax breakdown**: Individual tax groups and their amounts are removed
- **Maintains total amount**: The final total amount is still shown

## Installation

1. Copy the module to your Odoo addons directory
2. Update the apps list: `Settings > Apps > Update Apps List`
3. Search for "POS Hide Taxes"
4. Click Install

## Usage

Once installed, the module automatically modifies all POS receipts to hide:
- Tax breakdown section (subtotals and tax groups)
- Untaxed amounts
- Tax details

The receipt will show:
- Order lines with prices
- Total amount
- Payment information
- Change (if applicable)

## Technical Details

**Module Name**: `chaos_pos_hide_taxes`
**Version**: 18.0.1.0.0
**Depends on**: `point_of_sale`
**Category**: Point of Sale

### Implementation

The module uses template inheritance to extend the `point_of_sale.OrderReceipt` template:
- Removes the `pos-receipt-taxes` div element using XPath
- No backend modifications required
- Pure frontend customization

## Compatibility

- Odoo Version: 18.0
- Compatible with standard POS module
- Should work with most POS extensions that don't heavily modify receipt templates

## Author

Chaos

## License

LGPL-3
