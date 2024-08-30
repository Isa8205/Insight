window.addEventListener('scroll', function() {
    const sidebar = document.getElementById('sidebar');
    const footer = document.querySelector('.footer');
    const footerRect = footer.getBoundingClientRect();
    const sidebarRect = sidebar.getBoundingClientRect();
    const viewportHeight = window.innerHeight;
    
    if (footerRect.top < viewportHeight) {
        // If footer is visible in the viewport, move the sidebar above the footer
        sidebar.style.position = 'absolute';
        sidebar.style.bottom = `${window.scrollY + footerRect.top - sidebarRect.height - 10}px`;
    } else {
        // If footer is not visible, keep the sidebar fixed
        sidebar.removeAttribute('style')
        sidebar.classList.add('sidebar')
    }
});
