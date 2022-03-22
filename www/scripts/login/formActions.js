//Login function handler:
function login() {
	event.preventDefault();
	//Perform login:
	$.ajax({
		url: "/action/loginUser?" + $("#login-form").serialize(),
		method: "POST",
		statusCode: {
			200: function() {
				//Reload to trigger redirectToHome()
				location.reload(true);
			},
			401: function(xhr) {
				alert(xhr.responseText);
			}
		},
		fail: function() {
			alert("login(): Request Failed");
		}
	});
}

//Registration function handler:
function register() {
	event.preventDefault();
	//Get form data:
	let username = $("#register-username").val();
	let password = $("#register-password").val();
	let confirmPass = $("#confirm-password").val();
	//Check password match:
	if(password != confirmPass) {
		alert("Passwords do not match!");
		return;
	}
	//Perform registration:
	$.ajax({
		url: "/action/registerUser?username=" + username + "&password=" + password,
		method: "POST",
		statusCode: {
			200: function(xhr) {
				//Display success message
				alert(xhr);
				location.reload(true);
			},
			401: function(xhr) {
				//Display failure message
				alert(xhr.responseText + ": Account already exists!");
			}
		},
		fail: function() {
			alert("register(): Request failed");
		}
	});
}
