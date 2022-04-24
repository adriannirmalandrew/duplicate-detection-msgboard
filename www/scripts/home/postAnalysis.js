//Get trending topics from Twitter and their associated sentiments
function getTwitterTrendsSentiments() {
	//TODO
}

//Compute sentiments of given text
function computeNewPostSentiment(newPostContent) {
	$.ajax({
		url: "/action/computePostSentiment?content=" + newPostContent,
		method: "GET",
		statusCode: {
			200: function(sentiment_res) {
				return sentiment_res;
			},
		},
	});
}
//Handle sentiment computation button
function newPostSentimentAction() {
	let newPostContent = $("#new-post-content").val();
	let newPostSentiment = computeNewPostSentiment(newPostContent);
	//Set value in document element
	//TODO
}

//Get posts similar to user's new post
function getSimilarPosts() {
	//TODO
}
//Handle similar post button
function similarPostsAction() {
	//TODO
}

//Get trending topics on page load
$(document).ready(function() {
	//TODO
})