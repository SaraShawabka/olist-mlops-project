-- Olist MLOps Project
-- Data Validation Checks

-- ============================================================
-- 1. Row Counts
-- ============================================================

SELECT 'customers' AS table_name, COUNT(*) AS row_count
FROM customers

UNION ALL

SELECT 'orders', COUNT(*)
FROM orders

UNION ALL

SELECT 'order_items', COUNT(*)
FROM order_items

UNION ALL

SELECT 'order_payments', COUNT(*)
FROM order_payments

UNION ALL

SELECT 'order_reviews', COUNT(*)
FROM order_reviews

UNION ALL

SELECT 'products', COUNT(*)
FROM products

UNION ALL

SELECT 'sellers', COUNT(*)
FROM sellers

UNION ALL

SELECT 'geolocation', COUNT(*)
FROM geolocation

UNION ALL

SELECT 'product_category_translation', COUNT(*)
FROM product_category_translation;
-- ============================================================
-- 2. Foreign Key Integrity Checks
-- ============================================================

-- Orders without a matching customer
SELECT COUNT(*) AS orphan_orders
FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;


-- Order items without a matching order
SELECT COUNT(*) AS orphan_order_items
FROM order_items oi
LEFT JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;


-- Order items without a matching product
SELECT COUNT(*) AS orphan_order_items_products
FROM order_items oi
LEFT JOIN products p
    ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;


-- Order items without a matching seller
SELECT COUNT(*) AS orphan_order_items_sellers
FROM order_items oi
LEFT JOIN sellers s
    ON oi.seller_id = s.seller_id
WHERE s.seller_id IS NULL;


-- Payments without a matching order
SELECT COUNT(*) AS orphan_payments
FROM order_payments op
LEFT JOIN orders o
    ON op.order_id = o.order_id
WHERE o.order_id IS NULL;


-- Reviews without a matching order
SELECT COUNT(*) AS orphan_reviews
FROM order_reviews r
LEFT JOIN orders o
    ON r.order_id = o.order_id
WHERE o.order_id IS NULL;
-- ============================================================
-- 3. Primary Key & NULL Checks
-- ============================================================

-- Duplicate customer IDs
SELECT customer_id, COUNT(*) AS duplicate_count
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- Duplicate order IDs
SELECT order_id, COUNT(*) AS duplicate_count
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;


-- Duplicate product IDs
SELECT product_id, COUNT(*) AS duplicate_count
FROM products
GROUP BY product_id
HAVING COUNT(*) > 1;


-- Duplicate seller IDs
SELECT seller_id, COUNT(*) AS duplicate_count
FROM sellers
GROUP BY seller_id
HAVING COUNT(*) > 1;


-- NULL customer IDs
SELECT COUNT(*) AS null_customer_ids
FROM customers
WHERE customer_id IS NULL;


-- NULL order IDs
SELECT COUNT(*) AS null_order_ids
FROM orders
WHERE order_id IS NULL;


-- NULL product IDs
SELECT COUNT(*) AS null_product_ids
FROM products
WHERE product_id IS NULL;


-- NULL seller IDs
SELECT COUNT(*) AS null_seller_ids
FROM sellers
WHERE seller_id IS NULL;
