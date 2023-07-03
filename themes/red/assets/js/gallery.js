imagesLoaded(document.querySelector('.grid'), function(instance) {
    new Masonry('.grid', {
        itemSelector: '.grid-item',
        columnWidth: '.grid-sizer',
        percentPosition: true,
        gutter: '.gutter-sizer'
    });
});

imagesLoaded(document.querySelector('.second-grid'), function(instance) {
    new Masonry('.second-grid', {
        itemSelector: '.grid-item',
        columnWidth: '.grid-sizer',
        percentPosition: true,
        gutter: '.gutter-sizer'
    });
});
