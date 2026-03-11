document.addEventListener('DOMContentLoaded', function() {
    loadCharte();
    loadTheme();
    loadMode();
    setupCharteSelector();
    setupThemeSelector();
    setupModeSelector();
    setupFamicloudThemeDropdown();
    checkCookieConsent();
});

const FAMICLOUD_MODES = ['hyper-econome', 'econome', 'normal'];

function loadCharte() {
    const saved = localStorage.getItem('charte') || 'famicloud';
    applyCharte(saved);
}

function applyCharte(charte) {
    document.documentElement.setAttribute('data-charte', charte);

    document.querySelectorAll('.charte-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.charte === charte);
    });

    const famiSelector = document.querySelector('.famicloud-theme-selector');
    if (famiSelector) {
        famiSelector.style.display = charte === 'famicloud' ? 'flex' : 'none';
    }

    if (charte === 'famicloud') {
        const currentMode = localStorage.getItem('displayMode') || 'normal';
        if (!FAMICLOUD_MODES.includes(currentMode)) {
            setMode('normal');
        }
        const famiTheme = localStorage.getItem('famicloud-theme') || 'ocean-profond';
        setTheme(famiTheme);
    } else {
        const jguTheme = localStorage.getItem('jgu-theme') || 'nuit-foret';
        setTheme(jguTheme);
    }
}

function setCharte(charte) {
    localStorage.setItem('charte', charte);
    applyCharte(charte);
}

function setupCharteSelector() {
    document.querySelectorAll('.charte-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            setCharte(this.dataset.charte);
        });
    });
}

function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'nuit-foret';
    document.documentElement.setAttribute('data-theme', savedTheme);

    document.querySelectorAll('.theme-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.theme === savedTheme);
    });
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);

    const charte = document.documentElement.getAttribute('data-charte') || 'jgu';
    if (charte === 'famicloud') {
        localStorage.setItem('famicloud-theme', theme);
    } else {
        localStorage.setItem('jgu-theme', theme);
    }

    document.querySelectorAll('.theme-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.theme === theme);
    });
}

function setupThemeSelector() {
    document.querySelectorAll('.theme-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            setTheme(this.dataset.theme);
        });
    });
}

function loadMode() {
    const savedMode = localStorage.getItem('displayMode') || 'econome';
    document.documentElement.setAttribute('data-mode', savedMode);

    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === savedMode);
    });
}

function setMode(mode) {
    document.documentElement.setAttribute('data-mode', mode);
    localStorage.setItem('displayMode', mode);

    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });
}

function setupModeSelector() {
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            setMode(this.dataset.mode);
        });
    });
}

function setupFamicloudThemeDropdown() {
    const trigger = document.getElementById('famicloud-theme-trigger');
    const dropdown = document.getElementById('famicloud-theme-dropdown');
    if (!trigger || !dropdown) return;

    trigger.addEventListener('click', function(e) {
        e.stopPropagation();
        const isOpen = dropdown.classList.toggle('open');
        trigger.setAttribute('aria-expanded', isOpen);
    });

    document.addEventListener('click', function() {
        dropdown.classList.remove('open');
        trigger.setAttribute('aria-expanded', 'false');
    });

    dropdown.addEventListener('click', function(e) {
        e.stopPropagation();
    });
}

function autoHideNotifications() {
    const notifications = document.querySelectorAll('.notification');
    notifications.forEach(notif => {
        setTimeout(() => {
            notif.style.opacity = '0';
            setTimeout(() => notif.remove(), 300);
        }, 5000);
    });
}

document.addEventListener('DOMContentLoaded', autoHideNotifications);

function checkCookieConsent() {
    const consent = localStorage.getItem('cookie_consent');
    if (consent === null) {
        showCookieBanner();
    } else if (consent === 'accepted') {
        initTracking();
    }
}

function showCookieBanner() {
    const banner = document.getElementById('cookie-banner');
    if (banner) {
        banner.style.display = 'block';
    }
}

function hideCookieBanner() {
    const banner = document.getElementById('cookie-banner');
    if (banner) {
        banner.style.display = 'none';
    }
}

function acceptCookies() {
    localStorage.setItem('cookie_consent', 'accepted');
    hideCookieBanner();
    initTracking();
}

function refuseCookies() {
    localStorage.setItem('cookie_consent', 'refused');
    hideCookieBanner();
}

function hasTrackingConsent() {
    return localStorage.getItem('cookie_consent') === 'accepted';
}

function initTracking() {
    if (!hasTrackingConsent()) return;
    trackPageView();
    trackClicks();
    trackFormInputs();
    trackScroll();
}

function sendLog(data) {
    if (!hasTrackingConsent()) return;
    fetch('/api/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).catch(() => {});
}

function getElementSelector(el) {
    if (el.id) return '#' + el.id;
    if (el.className) return el.tagName.toLowerCase() + '.' + el.className.split(' ').join('.');
    return el.tagName.toLowerCase();
}

function trackPageView() {
    sendLog({
        type: 'pageview',
        page: window.location.pathname,
        element: null,
        details: { referrer: document.referrer, title: document.title }
    });
}

function trackClicks() {
    document.addEventListener('click', function(e) {
        const target = e.target.closest('a, button, input[type="submit"], .nav-link, .btn');
        if (!target) return;
        sendLog({
            type: 'click',
            page: window.location.pathname,
            element: getElementSelector(target),
            details: { text: target.textContent.trim().substring(0, 50), href: target.href || null }
        });
    });
}

function trackFormInputs() {
    document.addEventListener('change', function(e) {
        const target = e.target;
        if (!['INPUT', 'SELECT', 'TEXTAREA'].includes(target.tagName)) return;
        const isSensitive = ['password', 'email'].includes(target.type) || target.name === 'password';
        sendLog({
            type: 'input',
            page: window.location.pathname,
            element: getElementSelector(target),
            details: {
                field: target.name || target.id,
                type: target.type,
                value: isSensitive ? '[masque]' : target.value.substring(0, 100)
            }
        });
    });
}

let scrollTimeout;
function trackScroll() {
    window.addEventListener('scroll', function() {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(function() {
            const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
            sendLog({
                type: 'scroll',
                page: window.location.pathname,
                element: null,
                details: { percent: scrollPercent }
            });
        }, 1000);
    });
}
