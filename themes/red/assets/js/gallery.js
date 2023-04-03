imagesLoaded(document.querySelector('.grid'), function(instance) {
    new Masonry('.grid', {
        itemSelector: '.grid-item',
        columnWidth: '.grid-sizer',
        fitWidth: true,
        gutter: 10,
    });
});
