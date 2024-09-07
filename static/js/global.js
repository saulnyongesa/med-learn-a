const getScreenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

const tutorial_nav_vertical = document.getElementById('tutorial-nav-vertical');

function hideVarticalTutorialTopicNavs() {
    if (getScreenWidth < 768) {
        tutorial_nav_vertical.classList.add('d-none')
    } else {
        tutorial_nav_vertical.classList.remove('d-none')
    }    
}
window.onresize = hideVarticalTutorialTopicNavs
window.onload = hideVarticalTutorialTopicNavs
