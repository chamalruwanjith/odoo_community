# Sale Project Subtask Automation

## Overview

This module extends Odoo's `sale_project` functionality to automatically create subtasks based on product configuration when sale orders are confirmed.

## Features

- ✅ **Subtask Template Configuration**: Define subtask templates directly on products
- ✅ **Automatic Creation**: Subtasks are automatically created when tasks are generated from sale orders
- ✅ **Full Integration**: Seamlessly integrates with existing sale_project workflow
- ✅ **Flexible Configuration**: Configure name, sequence, allocated hours, and description for each subtask
- ✅ **Smart Inheritance**: Subtasks automatically inherit project, customer, and sale order from parent task
- ✅ **Clean UI**: Subtasks are hidden from project board and only visible within parent task

## Installation

1. Copy the `vkd_sale_project_subtask` module to your Odoo addons directory
2. Update the app list: Go to Apps → Update Apps List
3. Search for "Sale Project Subtask Automation"
4. Click Install

## Configuration

### 1. Configure Product with Subtask Templates

1. Go to **Sales → Products → Products**
2. Open a product (or create new one)
3. Set **Service Tracking** to either:
   - "Create a task in an existing project" (`task_global_project`)
   - "Create a task in sales order's project" (`task_in_project`)
4. Go to the **Subtask Templates** tab
5. Add subtask templates:
   - **Sequence**: Order of subtasks
   - **Subtask Name**: Name for the subtask
   - **Allocated Hours**: Hours allocated for this subtask
   - **Description**: Detailed instructions or requirements
   - **Active**: Toggle to enable/disable template

### 2. Manage Subtask Templates Globally

You can also manage all subtask templates from:
**Sales → Configuration → Products → Subtask Templates**

## Usage

### Workflow Example

1. **Setup Product**:
   ```
   Product: Website Development
   Service Tracking: Create a task in sales order's project

   Subtask Templates:
   ├─ Requirements Analysis (8 hours)
   ├─ UI/UX Design (16 hours)
   ├─ Development (40 hours)
   ├─ Testing & QA (16 hours)
   └─ Deployment (8 hours)
   ```

2. **Create Sale Order**:
   - Add "Website Development" product to sale order
   - Confirm the sale order

3. **Automatic Result**:
   - ✅ Project created (if using task_in_project mode)
   - ✅ Main task created: "Website Development"
   - ✅ 5 subtasks created automatically:
     - Requirements Analysis (8 hours)
     - UI/UX Design (16 hours)
     - Development (40 hours)
     - Testing & QA (16 hours)
     - Deployment (8 hours)

### Subtask Properties

Each automatically created subtask has:
- **Parent Task**: Linked to main task
- **Project**: Same as parent task
- **Customer**: Same as parent task
- **Sale Order**: Linked to same SO
- **Sale Order Line**: Linked to same SO line
- **Allocated Hours**: From template configuration
- **Description**: From template configuration
- **Display in Project**: False (hidden from project board, visible in parent task only)

## Technical Details

### Models

#### `product.subtask.template`
- Main model for storing subtask templates
- Fields:
  - `name`: Subtask name (required, translatable)
  - `product_tmpl_id`: Related product (required)
  - `sequence`: Display order (default: 10)
  - `allocated_hours`: Hours for subtask
  - `description`: Detailed description (HTML)
  - `active`: Enable/disable template

#### `product.template` (inherited)
- Added field: `subtask_template_ids` (One2many)
- Added computed field: `subtask_template_count`

#### `sale.order.line` (inherited)
- Overridden method: `_timesheet_create_task()`
- New method: `_create_subtasks_from_templates()`
- New method: `_prepare_subtask_values()`

### Key Methods

```python
def _timesheet_create_task(self, project):
    """Override to create subtasks after main task creation"""
    task = super()._timesheet_create_task(project)
    if task and self.product_id.subtask_template_ids:
        self._create_subtasks_from_templates(task)
    return task

def _create_subtasks_from_templates(self, parent_task):
    """Create subtasks from product templates"""
    # Batch create all subtasks
    # Post message on parent task
    return subtasks
```

## Dependencies

- `sale_project`
- `project`

## Author

**Your Company**

## License

LGPL-3

## Support

For issues or feature requests, please contact your system administrator.

---

**Version**: 18.0.1.0.0
**Category**: Sales/Sales
**Odoo Version**: 18.0
