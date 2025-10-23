//main.js

document.addEventListener('DOMContentLoaded', function () {
    if (typeof bootstrap === 'undefined' || typeof bootstrap.Collapse === 'undefined') {
        return;
    }

    const toggles = document.querySelectorAll('.category-toggle');
    toggles.forEach(function (toggle) {
        const targetSelector = toggle.getAttribute('data-bs-target');
        if (!targetSelector) return;

        const targetEl = document.querySelector(targetSelector);
        if (!targetEl) return;

        const icon = toggle.querySelector('.category-toggle-icon');
        const collapseInstance = bootstrap.Collapse.getOrCreateInstance(targetEl, { toggle: false });

        toggle.addEventListener('click', function (event) {
            event.preventDefault();
            event.stopPropagation();

            if (targetEl.classList.contains('show')) {
                collapseInstance.hide();
            } else {
                collapseInstance.show();
            }
        });

        targetEl.addEventListener('shown.bs.collapse', function () {
            toggle.setAttribute('aria-expanded', 'true');
            if (icon) icon.textContent = '–';
        });

        targetEl.addEventListener('hidden.bs.collapse', function () {
            toggle.setAttribute('aria-expanded', 'false');
            if (icon) icon.textContent = '☰';
        });
    });
});