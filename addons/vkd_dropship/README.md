# VKD Dropship Management Module

## Overview

This module extends Odoo's standard dropshipping functionality to provide more flexibility and control over dropship processes. It allows products to be configured for both standard sales and dropship, with the ability to choose the delivery method per sale order.

## Features

1. **Create Sale Orders from Purchase Orders** - Link SOs to existing POs to prevent duplicate PO creation
2. **Optional Dropship per Order** - Choose dropship vs. standard delivery per SO, regardless of product configuration
3. **Dropship Quantity Tracking** - Track how much of a PO has been dropshipped vs. received
4. **Smart Buttons** - View all linked SOs from PO and vice versa

## Installation

1. Copy the `vkd_dropship` module to your Odoo addons directory
2. Update the apps list: Apps → Update Apps List
3. Search for "VKD Dropship Management"
4. Click "Install"

## Configuration

### Product Setup

Products should be configured with the **Dropship** route if they support dropshipping:

1. Go to Inventory → Products → Products
2. Select a product (e.g., Diesel)
3. Go to Inventory tab
4. In **Routes**, check "Dropship"
5. Add vendor in the **Purchase** tab

Products can have BOTH dropship route and standard delivery routes enabled, allowing flexibility per order.

## Usage Scenarios

### Scenario 1: Create SO from Existing PO

**Use Case**: You have a large PO (e.g., P001 for 100,000L diesel) and want to create SOs for customers without creating new POs.

**Steps**:

1. **Create Large Purchase Order**
   - Go to Purchase → Orders → Create
   - Add product: Diesel, Qty: 100,000 L
   - Confirm PO (P001)

2. **Create Sale Order from PO**
   - Option A: From PO form, click "Create SO" button
   - Option B: Create new SO manually

3. **Link SO to Existing PO**
   - In SO form, check **"Is Dropship Order"**
   - In **"Source Purchase Order"** field, select P001
   - Add order line: Diesel, 2000 L

4. **Confirm Sale Order**
   - System will NOT create a new PO
   - Instead, it links to P001 and creates dropship picking directly
   - Customer receives diesel from P001

5. **View Dropship Status on PO**
   - Open P001
   - See **"Dropship Delivered Qty"**: 2000 L (after validation)
   - See **"Remaining Quantity"**: 98,000 L
   - Click **"Linked SOs"** smart button to see all related SOs

### Scenario 2: Direct Sale (Not Dropship) for Dropship Product

**Use Case**: Diesel supports both dropship and direct sale. Customer B wants direct delivery (not dropship).

**Steps**:

1. **Create Sale Order**
   - Go to Sales → Orders → Create
   - Customer: Customer B
   - **UNCHECK** "Is Dropship Order" (or leave it unchecked)
   - Add product: Diesel, 5000 L

2. **Confirm Sale Order**
   - Even though Diesel has dropship route, the system will use standard delivery
   - Creates delivery order from your warehouse to customer
   - NO purchase order is created

3. **Deliver from Warehouse**
   - Standard delivery process continues
   - Inventory is deducted from your warehouse

### Scenario 3: Standard Dropship for Dropship-Only Product

**Use Case**: Petrol is configured as dropship-only. Customer B wants 4000L.

**Steps**:

1. **Create Sale Order**
   - Go to Sales → Orders → Create
   - Customer: Customer B
   - **CHECK** "Is Dropship Order"
   - Leave **"Source Purchase Order"** empty (not linked to existing PO)
   - Add product: Petrol, 4000 L

2. **Confirm Sale Order**
   - System follows standard Odoo dropship process
   - Creates NEW purchase order automatically
   - Dropship picking is created (Supplier → Customer)

3. **Standard Dropship Flow**
   - Confirm PO
   - Validate dropship picking
   - Customer receives directly from supplier

## Field Reference

### Sale Order Fields

| Field | Description |
|-------|-------------|
| **Is Dropship Order** | Check to enable dropship for this order. Uncheck for standard delivery even if product has dropship route |
| **Source Purchase Order** | Link to existing PO to prevent creating new PO. Automatically sets "Is Dropship Order" to True |
| **Linked to PO** | Technical field indicating if SO is linked to a source PO |

### Sale Order Line Fields

| Field | Description |
|-------|-------------|
| **Is Dropship** | Computed field showing if line will be dropshipped |
| **Source PO Line** | Link to specific PO line from source PO |

### Purchase Order Fields

| Field | Description |
|-------|-------------|
| **Total Dropship Quantity** | Total quantity delivered via dropship |
| **Reserved Dropship Quantity** | Quantity reserved for linked SOs (not yet delivered) |
| **Remaining Quantity** | Quantity available to receive or dropship |
| **Linked Sale Orders** | One2many field showing all linked SOs |
| **Linked SO Count** | Number of linked SOs (for smart button) |

### Purchase Order Line Fields

| Field | Description |
|-------|-------------|
| **Dropship Delivered Qty** | Quantity delivered via dropship for this line |
| **Dropship Reserved Qty** | Quantity reserved for dropship (in SO but not delivered) |
| **Source Sale Lines** | Sale order lines linked to this PO line |

## Smart Buttons

### On Sale Order
- **Source PO**: View the source purchase order (if linked)

### On Purchase Order
- **Linked SOs**: View all sale orders linked to this PO
- **Create SO**: Quick action to create a new SO from this PO

## Technical Details

### Models Extended
- `sale.order`
- `sale.order.line`
- `purchase.order`
- `purchase.order.line`
- `stock.picking`
- `stock.move`

### Key Methods Overridden
- `sale.order.line._action_launch_stock_rule()` - Handles custom procurement logic
- `stock.picking.button_validate()` - Updates dropship quantities on validation
- `stock.move._action_done()` - Recomputes dropship quantities when moves complete

## Dependencies

- sale
- purchase
- stock
- sale_stock
- purchase_stock
- stock_dropshipping
- sale_purchase
- sale_purchase_stock

## Support

For issues or questions, please contact VKD support.

## License

LGPL-3

## Version

18.0.1.0.0 (Odoo 18.0)
