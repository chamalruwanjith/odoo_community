/** @odoo-module **/

// Limit quantity to 1 for specific subscription upsell products
document.addEventListener('DOMContentLoaded', function() {
    const limitedProductKeys = ['allowExternalAPI', 'collectPeriod'];

    // Function to enforce quantity limit
    function enforceQuantityLimit($row) {
        const productKey = $row.dataset.productKey;
        if (!productKey || !limitedProductKeys.includes(productKey)) {
            return;
        }

        const $input = $row.querySelector('input[name^="line-"][name$="-quantity"]');
        if (!$input) return;

        const $plusBtn = $row.querySelector('.js_quantity.js_add');
        const $minusBtn = $row.querySelector('.js_quantity.js_remove');

        // Check current quantity
        const currentQty = parseInt($input.value || 0, 10);

        // Disable plus button if quantity >= 1
        if ($plusBtn) {
            if (currentQty >= 1) {
                $plusBtn.disabled = true;
                $plusBtn.classList.add('opacity-50', 'pe-none');
                $plusBtn.style.cursor = 'not-allowed';
            } else {
                $plusBtn.disabled = false;
                $plusBtn.classList.remove('opacity-50', 'pe-none');
                $plusBtn.style.cursor = 'pointer';
            }
        }

        // Prevent manual input above 1
        $input.addEventListener('input', function(e) {
            let value = parseInt(e.target.value || 0, 10);
            if (value > 1) {
                e.target.value = 1;
                // Trigger change event to update the order
                e.target.dispatchEvent(new Event('change', { bubbles: true }));
            }
        });

        // Intercept plus button clicks
        if ($plusBtn) {
            $plusBtn.addEventListener('click', function(e) {
                const qty = parseInt($input.value || 0, 10);
                if (qty >= 1) {
                    e.preventDefault();
                    e.stopPropagation();

                    // Show warning message
                    const $alert = document.createElement('div');
                    $alert.className = 'alert alert-warning alert-dismissible fade show mt-2';
                    $alert.innerHTML = `
                        <strong>Quantity Limit:</strong> Maximum quantity for this product is 1
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    `;

                    const $container = $row.closest('table');
                    if ($container && !$container.querySelector('.alert-warning')) {
                        $container.parentNode.insertBefore($alert, $container);
                        setTimeout(() => $alert.remove(), 3000);
                    }

                    return false;
                }
            }, true);
        }
    }

    // Apply to all existing rows
    function updateAllRows() {
        document.querySelectorAll('tr[data-product-key]').forEach(enforceQuantityLimit);
    }

    // Initial check
    updateAllRows();

    // Watch for dynamic changes (AJAX updates)
    const observer = new MutationObserver(updateAllRows);
    const targetNode = document.querySelector('.o_portal_sale_sidebar') || document.body;
    observer.observe(targetNode, { childList: true, subtree: true });
});
