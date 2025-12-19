=======================
POS Hide Taxes on Receipt
=======================

.. |badge1| image:: https://img.shields.io/badge/maturity-Production-green.png
    :target: https://odoo-community.org/page/development-status
    :alt: Production
.. |badge2| image:: https://img.shields.io/badge/licence-LGPL--3-blue.png
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-chaos__pos__hide__taxes-lightgray.png?logo=github
    :target: https://github.com/chamalruwanjith/odoo_community/tree/18.0/chaos_pos_hide_taxes
    :alt: chamalruwanjith/odoo_community

|badge1| |badge2| |badge3|

This module adds a configurable option to hide tax information from Point of Sale receipts.
Perfect for businesses that want cleaner, simplified receipts without tax breakdown details.

**Table of contents**

.. contents::
   :local:

Features
========

* **Configurable per POS**: Enable/disable tax hiding for each Point of Sale independently
* **Multi-company support**: Each POS configuration can have different settings
* **Clean receipts**: Hide tax breakdown, untaxed amounts, and tax details
* **Maintains total**: Final total amount is always displayed
* **Easy configuration**: Simple checkbox in POS Settings
* **No code required**: Pure UI configuration

Configuration
=============

After installation:

1. Go to ``Point of Sale → Configuration → Settings``
2. Select your Point of Sale from the dropdown
3. Scroll to **Bills & Receipts** section
4. Enable **Hide Taxes on Receipt** checkbox
5. Click **Save**
6. Close any open POS sessions
7. Open a new POS session to see the changes

Usage
=====

When Enabled
------------

Receipts will hide:

* Tax breakdown section (subtotals and tax groups)
* Untaxed amounts
* Individual tax details

Receipts will still show:

* Order lines with prices
* **Total amount** (with taxes included)
* Payment information
* Change amount
* All other receipt elements

When Disabled
-------------

Receipts display all tax information as normal (default Odoo behavior).

Multi-Company
-------------

Each Point of Sale configuration can have different settings.
In multi-company environments, create separate POS configs for each company,
and each can have its own tax display preference.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/chamalruwanjith/odoo_community/issues>`_.

In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/chamalruwanjith/odoo_community/issues/new?body=module:%20chaos_pos_hide_taxes%0Aversion:%2018.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Authors
-------

* Chaos

Contributors
------------

* Chamal Ruwanjith

Maintainers
-----------

This module is maintained by Chaos.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is part of the `chamalruwanjith/odoo_community <https://github.com/chamalruwanjith/odoo_community/tree/18.0/chaos_pos_hide_taxes>`_ project on GitHub.

You are welcome to contribute.
