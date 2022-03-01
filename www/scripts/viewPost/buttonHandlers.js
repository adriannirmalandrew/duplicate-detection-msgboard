function getPostId() {
	let urlParams = new URLSearchParams(window.location.search);
	return urlParams.get("post_id");
}

function deletePost() {
	//Get post ID
	let postId = getPostId();
	//Perform request
	$.ajax({
		url: "/action/deletePost?post_id=" + postId,
		method: "POST",
		statusCode: {
			200: function(resp) {
				alert(resp.responseText);
				window.location.replace("/home.html");
			},
			401: function(resp) {
				alert(resp.responseText + ": Not logged in!");
			}
			500: function(resp) {
				alert(resp.responseText);
			},
		},
	});
}

function reportPost() {
	//TODO
}
