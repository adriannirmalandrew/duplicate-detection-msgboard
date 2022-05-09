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
function actionNewPostSentiment() {
	let postContent = $("#new-post-content").val();
	let postSentiment = computeNewPostSentiment(postContent);
	//Set value in document element
	//TODO
	//Set value in post creation form
	let newPostSentimentInput = $("#new-post-sentiment");
	newPostSentimentInput.attr("value", postSentiment);
}

//Get similar posts from local database
function getSimilarPostsLocal() {
	//TODO
}
function actionGetSimilarLocal() {
	//TODO
}

//Get similar posts from Twitter
function getSimilarPostsTwitter() {
	//TODO
}
function actionGetSimilarTwitter() {
	//TODO
}

//Get trending topics from Twitter and their associated sentiments
function getTwitterSentiments() {
	//TODO
}
function displayTwitterSentiments() {
	//TODO
}

//Get trending topics on page load
$(document).ready(function() {
	//TODO
})