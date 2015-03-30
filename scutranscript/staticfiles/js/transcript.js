$(document).ready(function() {
	//check validity on page load
	validateSubmit();
	
	//listen for input editing to validate
	$('#paste_content').on('input', validateSubmit);
});

function validateSubmit() {
	if ($('#paste_content').val().length > 0) { 
		$('input[type="submit"]').prop('disabled', false);
	} else {
		$('input[type="submit"]').prop('disabled', true);
	}
}
