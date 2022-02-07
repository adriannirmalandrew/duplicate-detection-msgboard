//Handle logout action
function logout() {
	$.ajax({
		url: "/action/logoutUser",
		method: "POST",
		statusCode: {
			200: function() {
				//Reload to trigger sessionCheckRedirect()
				location.reload(true);
			},
			401: function(xhr) {
				alert(xhr.responseText);
			}
		},
		fail: function() {
			alert("logout(): Request failed!");
		}
	});
}
