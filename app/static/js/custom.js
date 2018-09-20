(function($){
    if ($(".btn-modal-user").length == 0) {
        return
    }
    $('.btn-modal-user').click(function() {
        let email  = $(this).attr('data-to-modal')
        $("#inp-user-delete").val(email)
	});
})(jQuery);
