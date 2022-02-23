function getPostData(postId) {
	$.ajax({
		url: "http://localhost/action/getPost?post_id=" + postId,
		method: "GET",
		statusCode: {
			200: function(postJson) {
				console.log(postJson);
			},
		},
	});
}

function getComments() {
	//TODO
}

$(document).ready(function() {
	let urlParams = new URLSearchParams(window.location.search);
	let postId = urlParams.get("post_id");
	getPostData(postId);
});
