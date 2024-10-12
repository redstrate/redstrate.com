imagesLoaded(document.querySelector('.grid'), function(instance) {
    var typeIcons = document.getElementsByClassName('gallery-type-icon-hidden');

    for(var i = 0; i < typeIcons.length; i++) {
        typeIcons[i].classList.remove("gallery-type-icon-hidden");
    }

    new Masonry('.grid', {
        itemSelector: '.grid-item',
        columnWidth: '.grid-sizer',
        gutter: '.gutter-sizer',
        transitionDuration: 0,
        resize: true
    });
});

const element = document.getElementsByClassName('second-grid');
if (element.length > 0) {
    imagesLoaded(document.querySelector('.second-grid'), function(instance) {
        new Masonry('.second-grid', {
            itemSelector: '.grid-item',
            columnWidth: '.grid-sizer',
            gutter: '.gutter-sizer',
            transitionDuration: 0,
            resize: true
        });
    });
}
