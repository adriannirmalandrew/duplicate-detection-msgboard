//Redirect to login page if user is not logged in
function sessionCheckRedirect() {
	$.ajax({
		url: "/action/validateSession",
		method: "POST",
		statusCode: {
			401: function(xhr) {
				window.location.replace("/index.html");
			}
		}
	});
}

$(document).ready(function() {
	sessionCheckRedirect();
});
