document.addEventListener('DOMContentLoaded', function() {
    loadTheme();
    loadMode();
    setupThemeSelector();
    setupModeSelector();
    checkCookieConsent();
});

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
