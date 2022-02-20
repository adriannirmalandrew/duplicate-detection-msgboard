function uploadPost() {
	event.preventDefault();
	//Get form data:
	let newPostData = new FormData($("#create-post-form")[0]);
	//Execute request:
	$.ajax({
		url: "/action/uploadPost",
		method: "POST",
		enctype: "multipart/form-data",
		data: newPostData,
		processData: false,
		contentType: false,
		statusCode: {
			200: function() {
				alert("Post Uploaded");
				location.reload(true);
			},
			401: function() {
				alert("Session Expired");
				location.reload(true);
			},
			500: function(xhr) {
				alert(xhr.responseText);
			},
		},
	});
}
