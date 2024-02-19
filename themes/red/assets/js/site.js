function checkWidth() {
    if (!window.matchMedia('(max-device-width: 768px)').matches) {
        document.getElementById("nav-menu").open = true;
    }
}

window.onresize = function() {
    checkWidth();
};
