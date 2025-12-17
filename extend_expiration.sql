-- SQL Script to extend Odoo database expiration
-- Usage: psql <database_name> -f extend_expiration.sql

-- Check current expiration settings
SELECT key, value
FROM ir_config_parameter
WHERE key IN ('database.expiration_date', 'database.expiration_reason', 'database.enterprise_code', 'database.create_date');

-- Update expiration date to 10 years from now
UPDATE ir_config_parameter
SET value = (CURRENT_DATE + INTERVAL '10 years')::text
WHERE key = 'database.expiration_date';

-- Clear expiration reason (or set to empty)
UPDATE ir_config_parameter
SET value = ''
WHERE key = 'database.expiration_reason';

-- If expiration_date doesn't exist, insert it
INSERT INTO ir_config_parameter (key, value, create_uid, create_date, write_uid, write_date)
SELECT 'database.expiration_date',
       (CURRENT_DATE + INTERVAL '10 years')::text,
       1,
       NOW(),
       1,
       NOW()
WHERE NOT EXISTS (SELECT 1 FROM ir_config_parameter WHERE key = 'database.expiration_date');

-- Verify the changes
SELECT key, value
FROM ir_config_parameter
WHERE key IN ('database.expiration_date', 'database.expiration_reason');
