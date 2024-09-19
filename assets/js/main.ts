document.addEventListener('DOMContentLoaded', () => {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    const firstId = anchorLinks[0]?.getAttribute('href');
    anchorLinks.forEach(anchor => {
        anchor.addEventListener('click', (event) => {
            event.preventDefault();
            const targetId = anchor.getAttribute('href');
            if (targetId) {
                const element = document.querySelector(targetId);
                if (element) {
                    element.scrollIntoView({ behavior: 'smooth' });
                    const uri = firstId == targetId ? '/' : `${targetId}`;
                    history.replaceState(undefined, '', uri)
                }
            }
        });
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const id = `#${entry.target.getAttribute('id')}`;
            if (entry.isIntersecting) {
                anchorLinks.forEach(anchor => {
                    if (anchor.getAttribute('href') === id) {
                        anchor.classList.add('active');
                    } else {
                        anchor.classList.remove('active');
                    }
                });
                const uri = firstId == id ? '/' : id;
                history.replaceState(undefined, '', uri);
            }
        });
    }, { threshold: 0.5 });

    const sections = document.querySelectorAll('section[id]');
    sections.forEach(section => {
        observer.observe(section);
    });
});
