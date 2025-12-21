/** @odoo-module **/
/**
 * ChaosHub Newsletter Subscription Handler
 * Handles AJAX form submission for newsletter subscriptions
 */

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.NewsletterSubscribe = publicWidget.Widget.extend({
    selector: '.js_subscribe_newsletter',
    events: {
        'submit': '_onSubmit',
    },

    /**
     * Handle newsletter form submission
     */
    async _onSubmit(ev) {
        ev.preventDefault();
        const $form = $(ev.currentTarget);
        const $email = $form.find('input[name="email"]');
        const $messageDiv = $form.find('.newsletter-message');
        const email = $email.val();

        if (!email || !this._validateEmail(email)) {
            this._showMessage($messageDiv, 'Please enter a valid email address', 'error');
            return;
        }

        try {
            const result = await jsonrpc('/newsletter/subscribe', {
                email: email,
            });

            if (result.success) {
                this._showMessage($messageDiv, result.message || 'Successfully subscribed!', 'success');
                $email.val('');
            } else {
                this._showMessage($messageDiv, result.message || 'Subscription failed', 'error');
            }
        } catch (error) {
            this._showMessage($messageDiv, 'An error occurred. Please try again.', 'error');
            console.error('Newsletter subscription error:', error);
        }
    },

    /**
     * Validate email address
     */
    _validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    /**
     * Show message to user
     */
    _showMessage($div, message, type) {
        $div.text(message)
            .removeClass('text-success text-danger')
            .addClass(type === 'success' ? 'text-success' : 'text-danger')
            .show();

        // Auto-hide after 5 seconds
        setTimeout(() => {
            $div.fadeOut();
        }, 5000);
    },
});

export default publicWidget.registry.NewsletterSubscribe;
