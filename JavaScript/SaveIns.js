var SI_query_hash = "";
var SI_id = window._sharedData.entry_data.ProfilePage[0].graphql.user.id;
var SI_first = "50";
var SI_url = "https://www.instagram.com/graphql/query/?query_hash="+SI_query_hash+"&variables=%7B%22id%22%3A%22"+SI_id+"%22%2C%22first%22%3A"+SI_first+"%7D";
var SI_xhr = new XMLHttpRequest();
SI_xhr.open("GET", SI_url, false);
SI_xhr.send();
var SI_responseJSON = JSON.parse(SI_xhr.responseText);
var SI_x;
var SI_y;
for (SI_x in SI_responseJSON.data.user.edge_owner_to_timeline_media.edges) {
	var SI_edge = SI_responseJSON.data.user.edge_owner_to_timeline_media.edges[SI_x];
	var SI_d_filename = SI_edge.node.taken_at_timestamp;
	var SI_d_url = "";
	if (SI_edge.node.is_video) {
		SI_d_filename += ".mp4";
		SI_d_url = SI_edge.node.video_url;
	} else {
		SI_d_filename += ".jpg";
		SI_d_url = SI_edge.node.display_url;
	}
	console.log(SI_d_filename + "\t" + SI_d_url);
	SI_download(SI_d_filename, SI_d_url);
	if (SI_edge.node.edge_sidecar_to_children != undefined) {
		for (SI_y in SI_edge.node.edge_sidecar_to_children.edges) {
			var SI_child_edge = SI_edge.node.edge_sidecar_to_children.edges[SI_y];
			var SI_child_d_filename = SI_d_filename + "_" + SI_y;
			var SI_child_d_url = "";
			if (SI_child_edge.node.is_video) {
				SI_child_d_filename += ".mp4";
				SI_child_d_url = SI_child_edge.node.video_url;
			} else {
				SI_child_d_filename += ".jpg";
				SI_child_d_url = SI_child_edge.node.display_url;
			}
			console.log(SI_child_d_filename + "\t" + SI_child_d_url);
			SI_download(SI_child_d_filename, SI_child_d_url);
		}
	}
}

function SI_download(filename, url) {
	fetch(url).then(SI_res => SI_res.blob().then(SI_blob => {
		var SI_atag = document.createElement("a");
		var SI_ObjURL = window.URL.createObjectURL(SI_blob);
		SI_atag.download = filename;
		SI_atag.href = SI_ObjURL;
		SI_atag.style.display = "none";
		document.body.appendChild(SI_atag);
		SI_atag.click();
		document.body.removeChild(SI_atag);
		window.URL.revokeObjectURL(SI_ObjURL);
	}))
};
