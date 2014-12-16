$(document).ready(function() {
    $('#paste_content').on('input', function(e) {
        if (this.value.length > 0) {
            $('button[type="submit"]').prop('disabled', false);
        } else {
            $('button[type="submit"]').prop('disabled', true);
        }
    });
});
