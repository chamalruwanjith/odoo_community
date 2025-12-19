# POS Hide Taxes

## Overview

This module adds a configurable option to hide tax-related information from Point of Sale receipts, providing a cleaner receipt format when needed.

## Features

- **Configurable per POS**: Enable/disable tax hiding for each Point of Sale separately
- **Multi-company support**: Each POS config can have different settings (POS configs are per-company)
- **Hides untaxed amount**: The subtotal without taxes is not displayed
- **Hides tax breakdown**: Individual tax groups and their amounts are removed
- **Maintains total amount**: The final total amount is still shown

## Installation

1. Copy the module to your Odoo addons directory
2. Update the apps list: `Settings > Apps > Update Apps List`
3. Search for "POS Hide Taxes"
4. Click Install

## Configuration

After installation, configure the setting for each Point of Sale:

1. Go to `Point of Sale > Configuration > Settings`
2. Select your Point of Sale from the dropdown at the top
3. Scroll to the **Bills & Receipts** section
4. Find the **Hide Taxes on Receipt** checkbox
5. Enable it to hide tax information from receipts
6. Click **Save**

**Note**: Each POS configuration can have different settings. In multi-company environments, create separate POS configs per company.

## Usage

### When Enabled

Receipts will hide:
- Tax breakdown section (subtotals and tax groups)
- Untaxed amounts
- Tax details

Receipts will still show:
- Order lines with prices
- Total amount
- Payment information
- Change (if applicable)

### When Disabled

Receipts will show all tax information as normal (default Odoo behavior).

## Technical Details

**Module Name**: `chaos_pos_hide_taxes`
**Version**: 18.0.1.0.0
**Depends on**: `point_of_sale`
**Category**: Point of Sale

### Implementation

The module extends the POS system with:

**Backend (Python)**:
- `pos.config` model: Adds `hide_receipt_taxes` boolean field (company_dependent)
- `res.config.settings` model: Adds related field for configuration UI

**Frontend (JavaScript)**:
- `PosOrder.export_for_printing()`: Patched to include the config setting in receipt data
- `order_receipt.xml`: Template inheritance to conditionally hide tax section based on setting

**Views**:
- Configuration UI in Point of Sale Settings (Bills & Receipts section)

### Database Fields

- **Field**: `hide_receipt_taxes`
- **Model**: `pos.config`
- **Type**: Boolean
- **Company Dependent**: No (pos.config is already per-company via company_id field)
- **Default**: False

## Compatibility

- Odoo Version: 18.0
- Compatible with standard POS module
- Should work with most POS extensions that don't heavily modify receipt templates

## Author

Chaos

## License

LGPL-3
