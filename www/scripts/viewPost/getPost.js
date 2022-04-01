function showButtons(isCreator) {
	//Show delete button is user is creator, else show report button
	if(isCreator) {
		$("#post-delete-button").attr("hidden", false);
	}
	else {
		$("#post-report-button").attr("hidden", false);
	}
}

function showPostActions(postJson) {
	//Validate session:
	$.ajax({
		url: "/action/validateSession",
		method: "POST",
		statusCode: {
			200: function() {
				//Check if user is the creator
				let isCreator = (Cookies.get("username") == postJson["creator"]);
				showButtons(isCreator);
			},
		},
	});
}

function showRepostWarning(postJson) {
	//Show banner and copied post's ID
	let postDuplicateDiv = $("#post-duplicate-div");
	postDuplicateDiv.attr("hidden", false);
	let copiedPostMsg = $("#copied-post-message");
	copiedPostMsg.html(copiedPostMsg.html() + postJson["copied_post"]);
}

function displayPostData(postJson) {
	//Show post ID and author
	let postTitle = $("#post-display-title");
	postTitle.html("Post " + postJson["post_id"] + " by " + postJson["creator"]);
	//Show content
	let postContent = $("#post-display-content");
	postContent.html("\"" + postJson["content"] + "\"");
	//Show image, if exists
	if(postJson["has_image"] == 1) {
		let postImageDiv = $("#post-display-image");
		let imageObj = $("<img>");
		imageObj.attr("src", "/images/" + postJson["post_id"]);
		imageObj.attr("height", 400);
		//imageObj.attr("width", 400);
		postImageDiv.append(imageObj);
	}
	//Show post actions if logged in:
	showPostActions(postJson);
	//Check if post is a duplicate:
	if(postJson["is_repost"] == 1) {
		showRepostWarning(postJson);
	}
}

function getPostData(postId) {
	$.ajax({
		url: "http://localhost/action/getPost?post_id=" + postId,
		method: "GET",
		statusCode: {
			200: function(postJson) {
				displayPostData(postJson);
			},
			404: function() {
				alert("Post not found!");
			}
		},
	});
}

$(document).ready(function() {
	let urlParams = new URLSearchParams(window.location.search);
	let postId = urlParams.get("post_id");
	getPostData(postId);
});
