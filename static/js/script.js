// Change navbar color on scroll
window.addEventListener('scroll', function() {
    const nav = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        nav.classList.add('bg-dark');
        nav.classList.remove('bg-transparent');
    } else {
        nav.classList.add('bg-transparent');
    }
});