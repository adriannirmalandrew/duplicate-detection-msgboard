function generateUserTable(usersData) {
	$("#registered-users-table").DataTable({
		"data": usersData,
		"columns": [
			{ "title": "Username" },
			{ "title": "Admin?" },
		],
	});
}

function getUserList() {
	//List of user data
	let usersData = [];
	//Get data and create links
	$.ajax({
		url: "/action/getAllUsers",
		method: "GET",
		success: function(usersRows) {
			for(row of usersRows) {
				let tempList = [];
				//User profile link
				let tempName = $("<a>");
				tempName.attr("href", "/viewProfile.html?user=" + row[0]);
				tempName.html(row[0]);
				tempList.push(tempName[0].outerHTML);
				//Is Admin?
				tempList.push(row[1]);
				//Add to row list
				usersData.push(tempList);
			};
			//Create DataTable
			generateUserTable(usersData);
		}
	});
}

function setCurrentUserName() {
	let username = Cookies.get("username");
	$("#header-username").html("Welcome, " + username);
}

$(document).ready(function() {
	setCurrentUserName();
	getUserList();
});
