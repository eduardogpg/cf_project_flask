$(document).ready(function(){
	
	console.log("Jquery form")

	function ajax_login(){
    $.ajax({
        url: '/ajax-login',
        data: $('form').serialize(),
        type: 'POST',
        success: function(response) {
					console.log(response);
        },
        error: function(error) {
					console.log(error);
        }
    });
	}	
	//No existe este id, si es necesario utilizar ajax debemos de quitar -test
    $( "#login-form-test" ).submit(function( event ) {
        event.preventDefault();
  	     ajax_login();
	});
	
});