package envoy.authz

import input.attributes.request.http as http_request

default allow = false

# Extract the current authenticated user
current_user = user {
	[_, payload] := split(http_request.headers.authorization, " ")
	[user, _] := split(base64url.decode(payload), ":")
}

# Allow access and determine the cluster based on the username and webtop service
allow {
	user := current_user
	path := split(http_request.path, "/")
	namespace := path[1] # Assumes URL format /<username>/<webtop>

	user == namespace
	webtop_service := path[2]

	# Check if the webtop service is one of the allowed services for the user
	webtop_service == user_webtop_clusters[user][_]
}

# Decision to emit headers indicating the cluster for routing
headers = {"X-Webtop-Cluster": webtop_cluster} {
	user := current_user
	path := split(http_request.path, "/")
	namespace := path[1]
	webtop_service := path[2]

	user == namespace
	webtop_cluster := user_webtop_clusters[user][webtop_service]
}

# Define allowed webtop services and corresponding clusters per user
user_webtop_clusters = {
	"user1": {"webtop1": "webtop1", "webtop1a": "webtop1a"},
	"user2": {"webtop2": "webtop2", "webtop2a": "webtop2a"},
}
