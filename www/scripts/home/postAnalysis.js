//Compute sentiments of given text
function displayNewPostSentiment(postSentimentValue) {
	//Set value in post creation form
	let newPostSentimentInput = $("#new-post-sentiment-input");
	newPostSentimentInput.attr("value", postSentimentValue);
	//Set value in analysis section
	let newPostSentiment = $("#post-sentiment-label");
	newPostSentiment.html("<b>Computed sentiment label: " + postSentimentValue + "</b>");
}
//Handle button action
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
function displaySimilarLocal() {
	//TODO
}
//Handle button action
function getSimilarPostsLocal() {
	//TODO
}

//Get similar posts from Twitter
function displaySimilarTwitter() {
	//TODO
}
//Handle button action
function getSimilarPostsTwitter() {
	//TODO
}

//Get trending topics from Twitter and their associated sentiments
function twitterSentimentTable(trendsJson) {
	//Generate data for table
	let trendsData = [];
	for(trend of Object.keys(trendsJson)) {
		//Topic
		trendRow = [];
		trendRow.push(trend);
		//Sentiments
		sentiments = trendsJson[trend];
		trendRow.push(sentiments["positive"]);
		trendRow.push(sentiments["neutral"]);
		trendRow.push(sentiments["negative"]);
		//Add to rows
		trendsData.push(trendRow);
	}
	//Create table
	$("#twitter-trend-sentiments-table").DataTable({
		"data": trendsData,
		"columns": [
			{"title": "Trend"},
			{"title": "Positive"},
			{"title": "Neutral"},
			{"title": "Negative"},
		],
	});
}
//Handle button action
function getTwitterSentiments() {
	//Make AJAX request
	$.ajax({
		url: "/action/twitterGetTrendsAndSentiments",
		method: "GET",
		statusCode: {
			200: function(trendsJson) {
				twitterSentimentTable(trendsJson);
			}
		},
	});
}

//Get trending topics on page load
$(document).ready(function() {
	//TODO
})