imagesLoaded(document.querySelector('.grid'), function(instance) {
    new Masonry('.grid', {
        itemSelector: '.grid-item',
        columnWidth: '.grid-sizer',
        percentPosition: true,
        gutter: '.gutter-sizer'
    });
});
