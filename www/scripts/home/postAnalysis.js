//Get trending topics from Twitter and their associated sentiments
function getTwitterSentiments() {
	//TODO
}
function displayTwitterSentiments() {
	//TODO
}

//Compute sentiments of given text
function computeNewPostSentiment(content) {
	$.ajax({
		url: "/action/computePostSentiment?content=" + content,
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
	let postContent = $("#new-post-content").val();
	let postSentiment = computeNewPostSentiment(postContent);
	//Set value in document element
	//TODO
	//Set value in post creation form
	let newPostSentimentInput = $("#new-post-sentiment");
	newPostSentimentInput.attr("value", postSentiment);
}

//Get posts similar to user's new post
function getSimilarPostsTwitter() {
	//TODO
}
function getSimilarPostsLocal() {
	//TODO
}
//Handle similar post button
function actionGetSimilarPosts() {
	//TODO
}

//Get trending topics on page load
$(document).ready(function() {
	//TODO
})