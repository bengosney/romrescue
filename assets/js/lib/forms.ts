export const initForms = () => {
    const forms = document.querySelectorAll<HTMLFormElement>('form[action][method="POST"]');

    forms.forEach(form => {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(form);
            const action = form.getAttribute('action');
            if (action) {
                const response = await fetch(action, { method: 'POST', body: formData });
                const rawHtml = await response.text();
                const parser = document.createElement('div');
                parser.innerHTML = rawHtml;
                const replacement = parser.querySelector('[data-replaces]');
                if (replacement) {
                    replacement.classList.add('is-replaced');
                    const target = document.querySelector(replacement.getAttribute('data-replaces') || '');
                    if (target) {
                        target.replaceWith(replacement);
                    }
                }
            }
        });
    });
};
