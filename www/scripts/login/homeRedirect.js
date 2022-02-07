//Redirect to home page if user is logged in
function redirectToHome() {
	$.ajax({
		url: "/action/validateSession",
		method: "POST",
		statusCode: {
			200: function(xhr) {
				window.location.replace("/home.html");
			}
		}
	});
}

$(document).ready(function() {
	redirectToHome();
});
