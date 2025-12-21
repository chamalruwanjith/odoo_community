/** @odoo-module **/
/**
 * ChaosHub Snippet JavaScript
 * Frontend interactions for custom snippets
 */

import publicWidget from "@web/legacy/js/public/public_widget";

// Smooth scroll for anchor links
publicWidget.registry.ChaosHubSmoothScroll = publicWidget.Widget.extend({
    selector: '.o_chaoshub_website',

    start() {
        this._super(...arguments);
        this._initSmoothScroll();
    },

    _initSmoothScroll() {
        this.$el.find('a[href^="#"]').on('click', (e) => {
            const href = $(e.currentTarget).attr('href');
            const $target = $(href);

            if ($target.length) {
                e.preventDefault();
                $('html, body').animate({
                    scrollTop: $target.offset().top - 80
                }, 600);
            }
        });
    },
});

// Lazy load images with intersection observer
publicWidget.registry.ChaosHubLazyLoad = publicWidget.Widget.extend({
    selector: '.o_chaoshub_website',

    start() {
        this._super(...arguments);
        this._initLazyLoad();
    },

    _initLazyLoad() {
        const images = this.el.querySelectorAll('img[loading="lazy"]');

        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                        }
                        observer.unobserve(img);
                    }
                });
            });

            images.forEach(img => imageObserver.observe(img));
        }
    },
});

export default {
    ChaosHubSmoothScroll: publicWidget.registry.ChaosHubSmoothScroll,
    ChaosHubLazyLoad: publicWidget.registry.ChaosHubLazyLoad,
};
