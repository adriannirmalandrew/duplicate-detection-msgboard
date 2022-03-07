function generatePostTable(postsData) {
	$("#user-posts-table").DataTable({
		"data": postsData,
		"columns": [
			{ "title": "Post ID" },
			{ "title": "Content" },
		]
	});
}

function getPostList(creator) {
	//List of posts data
	let postsData = [];
	//Get data and create links
	$.ajax({
		url: "/action/getUserPosts?creator=" + creator,
		method: "GET",
		success: function(postsRows) {
			for(row of postsRows) {
				let tempRow = [];
				//Link to post
				let tempLink = $("<a>");
				tempLink.attr("href", "/viewPost.html?post_id=" + row[0]);
				tempLink.html(row[0]);
				tempRow.push(tempLink[0].outerHTML);
				//Content of post
				tempRow.push(row[1]);
				//Add to row list
				postsData.push(tempRow);
			};
			//Create DataTable
			generatePostTable(postsData);
		},
	});
}

$(document).ready(function() {
	let creatorName = Cookies.get("username");
	getPostList(creatorName);
});
