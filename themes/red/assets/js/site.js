imagesLoaded(document.querySelector('.grid'), function(instance) {
    new Masonry('.grid', {
        itemSelector: '.grid-item',
        columnWidth: 300,
        fitWidth: true,
        gutter: 10
    });
});
