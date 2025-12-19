# Changelog

All notable changes to this module will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [18.0.1.0.0] - 2025-12-19

### Added
- Initial release for Odoo 18.0
- Configurable option to hide taxes from POS receipts
- Per-POS configuration via checkbox in Settings
- Multi-company support
- Conditional template rendering for tax sections
- JavaScript patch for PosOrder.export_for_printing()
- XML template inheritance for receipt customization
- Configuration UI in Point of Sale Settings (Bills & Receipts section)
- Professional README and documentation
- Odoo Apps Store listing preparation

### Features
- Hide tax breakdown section from receipts
- Hide untaxed amounts (subtotals)
- Maintain total amount display
- Simple checkbox configuration (no coding required)
- Compatible with standard POS module
- Clean and professional receipt format

### Technical
- Added `hide_receipt_taxes` Boolean field to `pos.config` model
- Added related field in `res.config.settings` for UI
- Template inheritance using XPath for conditional tax display
- PosOrder model patch to include config setting in receipt data
- Follows Odoo standard module structure

## [Future Releases]

### Planned
- Additional receipt customization options
- Support for hiding other receipt elements
- Receipt template presets
- Enhanced multi-language support

---

**Note:** This module is actively maintained. Please report issues on GitHub.
