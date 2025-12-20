/** @odoo-module **/

/**
 * ChaosHub.lk - Frontend JavaScript
 * Version: 1.0.0
 *
 * Optional interactive features for the website
 */

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.ChaosHubWebsite = publicWidget.Widget.extend({
    selector: '.o_chaoshub_website',

    /**
     * Initialize the widget
     */
    start: function () {
        this._super.apply(this, arguments);
        this._initSmoothScroll();
        this._initNewsletterForm();
    },

    /**
     * Initialize smooth scrolling for anchor links
     */
    _initSmoothScroll: function () {
        this.$el.find('a[href^="#"]').on('click', function (e) {
            const target = $(this.getAttribute('href'));
            if (target.length) {
                e.preventDefault();
                $('html, body').stop().animate({
                    scrollTop: target.offset().top - 80
                }, 600);
            }
        });
    },

    /**
     * Initialize newsletter form validation
     */
    _initNewsletterForm: function () {
        this.$el.find('.newsletter-form').on('submit', function (e) {
            const email = $(this).find('input[type="email"]').val();
            if (!email || !email.includes('@')) {
                e.preventDefault();
                alert('Please enter a valid email address');
                return false;
            }
        });
    },
});

export default publicWidget.registry.ChaosHubWebsite;
