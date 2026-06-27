/**
 * Aarohi AI - Landing Page Interactions
 * Provides premium animations, scroll reveals, animated statistics, and responsive mobile menu.
 */

document.addEventListener('DOMContentLoaded', () => {
    initStickyHeader();
    initMobileMenu();
    initScrollReveal();
    initStatsCounter();
});

/**
 * 1. Sticky Header Transparency Transition
 */
function initStickyHeader() {
    const header = document.querySelector('.landing-header');
    if (!header) return;

    const handleScroll = () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    };

    window.addEventListener('scroll', handleScroll);
    // Initial check
    handleScroll();
}

/**
 * 2. Mobile Menu Drawer & Toggle
 */
function initMobileMenu() {
    const toggleBtn = document.querySelector('.mobile-nav-toggle');
    const navLinksWrap = document.querySelector('.nav-links-wrap');
    const navLinks = document.querySelectorAll('.nav-link-landing');

    if (!toggleBtn || !navLinksWrap) return;

    toggleBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        navLinksWrap.classList.toggle('open');
        
        // Simple animation toggle for hamburger bar if desired
        toggleBtn.classList.toggle('active');
    });

    // Close menu when clicking on any section link
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navLinksWrap.classList.remove('open');
            toggleBtn.classList.remove('active');
        });
    });

    // Close menu when clicking outside of navbar
    document.addEventListener('click', (e) => {
        if (navLinksWrap.classList.contains('open') && !navLinksWrap.contains(e.target) && !toggleBtn.contains(e.target)) {
            navLinksWrap.classList.remove('open');
            toggleBtn.classList.remove('active');
        }
    });
}

/**
 * 3. IntersectionObserver Scroll Reveal Animations
 */
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.reveal');
    if (revealElements.length === 0) return;

    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -60px 0px',
        threshold: 0.1
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target); // Only trigger once
            }
        });
    }, observerOptions);

    revealElements.forEach(el => {
        revealObserver.observe(el);
    });
}

/**
 * 4. Statistics Counters Animation with Scroll Observer
 */
function initStatsCounter() {
    const statsContainer = document.querySelector('.impact-bg-wrap');
    const counters = document.querySelectorAll('.stat-number');
    if (!statsContainer || counters.length === 0) return;

    let animated = false;

    const startCounters = () => {
        counters.forEach(counter => {
            const targetAttr = counter.getAttribute('data-target');
            const suffix = counter.getAttribute('data-suffix') || '';
            const target = parseInt(targetAttr, 10);
            if (isNaN(target)) return;

            const duration = 1800; // ms
            const startTime = performance.now();

            const animateValue = (time) => {
                const elapsed = time - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                // Easing function: Ease Out Cubic
                const easeProgress = 1 - Math.pow(1 - progress, 3);
                
                const currentVal = Math.floor(easeProgress * target);
                
                if (target === 24 && suffix === '/7') {
                    counter.textContent = currentVal + suffix;
                } else {
                    counter.textContent = currentVal.toLocaleString() + suffix;
                }

                if (progress < 1) {
                    requestAnimationFrame(animateValue);
                } else {
                    // Final assignment to make sure it hits the exact target
                    if (target === 24 && suffix === '/7') {
                        counter.textContent = target + suffix;
                    } else {
                        counter.textContent = target.toLocaleString() + suffix;
                    }
                }
            };

            requestAnimationFrame(animateValue);
        });
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !animated) {
                animated = true;
                startCounters();
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    observer.observe(statsContainer);
}
