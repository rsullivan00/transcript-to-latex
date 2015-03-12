$(document).ready(function() {
    $('#paste_content').on('input', function(e) {
        if (this.value.length > 0) {
            $('input[type="submit"]').prop('disabled', false);
        } else {
            $('input[type="submit"]').prop('disabled', true);
        }
    });
});
