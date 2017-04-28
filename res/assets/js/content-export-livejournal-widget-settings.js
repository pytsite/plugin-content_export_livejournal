define(['jquery'], function ($) {
    return function (widget) {
        widget.em.find('#username').change(function () {
            widget.find('#title').val($(this).val());
        });
    }
});
