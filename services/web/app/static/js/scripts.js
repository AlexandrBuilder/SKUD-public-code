/*!
    * Start Bootstrap - SB Admin v6.0.0 (https://startbootstrap.com/templates/sb-admin)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/BlackrockDigital/startbootstrap-sb-admin/blob/master/LICENSE)
    */
(function ($) {
    "use strict";

    // Add active state to sidbar nav links
    var path = window.location.href; // because the 'href' property of the DOM element is the absolute path
    $("#layoutSidenav_nav .sb-sidenav a.nav-link").each(function () {
        if (this.href === path) {
            $(this).addClass("active");
        }
    });

    // Toggle the side navigation
    $("#sidebarToggle").on("click", function (e) {
        e.preventDefault();
        $("body").toggleClass("sb-sidenav-toggled");
    });

    $('.play-btn').on("click", function () {
        $('#video').empty();

        $('#video').append('<video controls width="100%"><source src="' + $(this).data('video') + '" id="video-source"></video>')
    })

    $(document).on('change', '.custom-file-input', function (event) {
        $(this).next('.custom-file-label').html(event.target.files[0].name);
    })

    setInterval(function() {
        const lastId = $('#main-id-events').find('tr').last().data('event-id');

        $.get('/last-events', {
            last_id: lastId
        }).done(function (response) {
            $(response).find('tr.line-event').each(function() {
              $('#main-id-events').find('tbody').last().append($( this ))
            });

            if ($(response).find('tr.line-event').length > 0) {
                $('.main-user-card-box').replaceWith($(response).find('.main-user-card-box'));
            }
        }).fail(function () {

        });
    }, 1000);
})(jQuery);
