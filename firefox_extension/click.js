browser.contextMenus.create({title: "Send to UniTrip",
                             contexts:["selection"],
                              onclick: function(info, tab){ sendSearch(info.selectionText, info.pageUrl); }
});


function sendSearch(text, url) {
	xhr = new XMLHttpRequest();
	var url = "http://localhost:5000/api/add";

	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.onreadystatechange = function () {
	    if (xhr.readyState == 4 && xhr.status == 200) {
	        var json = JSON.parse(xhr.responseText);
	        console.log(json);
	    }
	}
	var data = JSON.stringify({"text":text,"url":url});
	xhr.send(data);

}
