const screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
const nav_vertical = document.getElementById('nav-vertical');
const nav_vertical_hide_toggler = document.getElementById('nav-vertical-hide-toggler');
const nav_vertical_show_toggler = document.getElementById('nav-vertical-show-toggler');
const nav_horizontal = document.getElementById('nav-horizontal');
const nav_horizontal_logo_brand_holder = document.getElementById('nav-horizontal-logo-brand-holder');
const nav_items_horizontal = document.getElementById('nav-items-horizontal');

// Show Vertical Navbar
nav_vertical_show_toggler.addEventListener(
    'click',
    function () {
        nav_vertical.classList.remove('d-none')
        nav_vertical.classList.add('d-block')
        nav_vertical.style.zIndex = '1000'
        nav_horizontal_logo_brand_holder.classList.remove('d-flex')
        nav_horizontal_logo_brand_holder.classList.add('d-none')
    }
)
// Hide Vertical Navbar
nav_vertical_hide_toggler.addEventListener(
    'click',
    function () {
        nav_vertical.classList.remove('d-block')
        nav_vertical.classList.add('d-none')
        nav_horizontal_logo_brand_holder.classList.add('d-flex')
        nav_horizontal_logo_brand_holder.classList.remove('d-none')
    }
)

