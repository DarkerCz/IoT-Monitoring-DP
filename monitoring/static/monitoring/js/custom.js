$('[data-toggle="popover"]').popover();

$.extend( true, $.fn.dataTable.defaults, {
    "searching": false,
    "ordering": false,
    "language": {
      "url": '/static/monitoring/vendor/datatables/Czech.json'
    }
});

$('.password-toggle-btn').on('click', function(e){
    var input = $(this).closest('.input-group').find('input');
    if (input.attr('type') == 'text'){
        input.attr('type', 'password');
        $(this).html('<i class="far fa-eye"></i>');
    }
    else if (input.attr('type') == 'password'){
        input.attr('type', 'text');
        $(this).html('<i class="far fa-eye-slash"></i>');
    }
});

new ClipboardJS('.btn-copy');

$('.reload-content').on('click', function(e){
    e.preventDefault();
    $('[data-toggle="popover"]').popover('hide');
    $(this).closest('.card').find('.panel-body').reloadContent();
});