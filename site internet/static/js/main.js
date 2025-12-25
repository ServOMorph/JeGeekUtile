document.addEventListener('DOMContentLoaded', function() {
    loadTheme();
    loadMode();
    setupThemeSelector();
    setupModeSelector();
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
