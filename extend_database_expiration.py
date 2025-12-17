#!/usr/bin/env python3
"""
Script to extend Odoo database expiration date
Usage: python3 extend_database_expiration.py -d <database_name> -y <years_to_extend>
"""
import argparse
import sys
from datetime import datetime, timedelta
from xmlrpc import client as xmlrpclib

def extend_expiration(url, db, username, password, years=10):
    """
    Extend database expiration date

    Args:
        url: Odoo server URL (e.g., http://localhost:8069)
        db: Database name
        username: Admin username
        password: Admin password
        years: Number of years to extend (default: 10)
    """
    common = xmlrpclib.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})

    if not uid:
        print("Authentication failed!")
        return False

    models = xmlrpclib.ServerProxy(f'{url}/xmlrpc/2/object')

    # Calculate new expiration date
    new_expiration = datetime.now() + timedelta(days=365 * years)
    expiration_str = new_expiration.strftime('%Y-%m-%d')

    # Update system parameters
    try:
        # Set expiration date
        models.execute_kw(db, uid, password,
            'ir.config_parameter', 'set_param',
            ['database.expiration_date', expiration_str])

        # Set expiration reason to empty or 'extended'
        models.execute_kw(db, uid, password,
            'ir.config_parameter', 'set_param',
            ['database.expiration_reason', ''])

        print(f"✓ Database expiration extended to: {expiration_str}")
        print(f"✓ Expiration reason cleared")
        return True

    except Exception as e:
        print(f"Error updating parameters: {e}")
        return False

def check_expiration(url, db, username, password):
    """Check current database expiration status"""
    common = xmlrpclib.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})

    if not uid:
        print("Authentication failed!")
        return

    models = xmlrpclib.ServerProxy(f'{url}/xmlrpc/2/object')

    try:
        params = models.execute_kw(db, uid, password,
            'ir.config_parameter', 'search_read',
            [[['key', 'in', ['database.expiration_date', 'database.expiration_reason', 'database.enterprise_code']]]],
            {'fields': ['key', 'value']})

        print("\n=== Current Database Expiration Status ===")
        for param in params:
            print(f"{param['key']}: {param['value']}")
        print()

    except Exception as e:
        print(f"Error reading parameters: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extend Odoo database expiration')
    parser.add_argument('-u', '--url', default='http://localhost:8069', help='Odoo server URL')
    parser.add_argument('-d', '--database', required=True, help='Database name')
    parser.add_argument('-U', '--username', default='admin', help='Admin username')
    parser.add_argument('-p', '--password', required=True, help='Admin password')
    parser.add_argument('-y', '--years', type=int, default=10, help='Years to extend (default: 10)')
    parser.add_argument('-c', '--check', action='store_true', help='Only check current expiration')

    args = parser.parse_args()

    if args.check:
        check_expiration(args.url, args.database, args.username, args.password)
    else:
        check_expiration(args.url, args.database, args.username, args.password)
        extend_expiration(args.url, args.database, args.username, args.password, args.years)
        check_expiration(args.url, args.database, args.username, args.password)
