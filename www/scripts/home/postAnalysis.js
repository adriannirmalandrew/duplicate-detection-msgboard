//Compute sentiments of given text
function displayNewPostSentiment(postSentimentValue) {
	//Set value in post creation form
	let newPostSentimentInput = $("#new-post-sentiment-input");
	newPostSentimentInput.attr("value", postSentimentValue);
	//Set value in analysis section
	let newPostSentiment = $("#post-sentiment-label");
	newPostSentiment.html("<b>Computed sentiment label: " + postSentimentValue + "</b>");
}
//Handle butotn action
function computeNewPostSentiment() {
	//Get new post content
	let postContent = $("#new-post-content").val();
	//Make AJAX request
	$.ajax({
		url: "/action/computePostSentiment?content=" + postContent,
		method: "GET",
		statusCode: {
			200: function(sentiment_res) {
				displayNewPostSentiment(sentiment_res);
			},
		},
	});
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