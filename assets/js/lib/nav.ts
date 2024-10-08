export const initNav = () => {
    const anchorLinks: NodeListOf<HTMLAnchorElement> = document.querySelectorAll('a[href^="#"]');
    const firstId: string | null = anchorLinks[0]?.getAttribute('href');
    const navToggle: HTMLInputElement|null = document.querySelector('#nav-toggle');

    anchorLinks.forEach(anchor => {
        anchor.addEventListener('click', (event) => {
            event.preventDefault();
            navToggle && (navToggle.checked = false);
            const targetId = anchor.getAttribute('href');
            if (targetId) {
                const element = document.querySelector(targetId);
                if (element) {
                    element.scrollIntoView({ behavior: 'smooth' });
                    const uri: string = firstId == targetId ? '/' : `${targetId}`;
                    history.replaceState(undefined, '', uri)
                }
            }
        });
    });

    document.querySelectorAll('.back-to-top').forEach(anchor => {
        anchor.addEventListener('click', (event) => {
            event.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
            history.replaceState(undefined, '', '/');
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

};
