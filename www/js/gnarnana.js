function setNavPosition({backgroundIsAwlaysBlack = false} = {}) {
    var $nav = $('#main-nav');
    var navTop = $nav.offset().top
    function setNavPosition() {
        var scrollPosition = window.scrollY;
        var windowHeight = window.innerHeight;
        $nav.toggleClass('position-fixed', scrollPosition > navTop);
        if (!backgroundIsAwlaysBlack) {
            $nav.toggleClass('background-gradient-black', scrollPosition >= windowHeight);
        }
    }

    $(function() {
        $(window).on('scroll resize', setNavPosition);
        setNavPosition();
    });
}