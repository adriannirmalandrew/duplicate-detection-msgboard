//Login function handler:
function login() {
	event.preventDefault();
	//Get form data:
	let username = $("#login-username").val();
	let password = $("#login-password").val();
	//Perform login:
	$.ajax({
		url: "/action/loginUser?username=" + username + "&password=" + password,
		method: "POST",
		success: function() {
			location.reload(true);
		},
		fail: function() {
			alert("Failed to login");
		}
	});
}

//Registration function handler:
function register() {
	event.preventDefault();
	//Get form data:
	let username = $("register-username").val();
	let password = $("register-password").val();
	let confirmPass = $("confirm-password").val();
	//Check password match:
	if(password != confirmPass) {
		alert("Passwords do not match!");
		return;
	}
	//Perform registration:
	$.ajax({
		url: "/action/registerUser?username=" + username + "&password=" + password,
		method: "POST",
		success: function() {
			alert("Account Created");
			location.reload(true);
		},
		fail: function() {
			alert("Registration failed");
		}
	});
}
