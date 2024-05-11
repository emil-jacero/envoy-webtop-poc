package envoy.authz

import input.attributes.request.http as http_request

default allow = false

# Extract the current authenticated user
current_user = user {
    [_, payload] := split(http_request.headers.authorization, " ")
    [user, _] := split(base64url.decode(payload), ":")
}

# Decision to emit headers
response_headers = {"X-Webtop-Cluster": webtop_cluster} {
    user := current_user
    path := split(http_request.path, "/")
    namespace := path[1]
    webtop_service := path[2]

    user == namespace
    webtop_cluster := user_webtop_clusters[user][webtop_service]
}

# Map of users to their webtop services and corresponding clusters
user_webtop_clusters = {
    "user1": {"webtop1": "cluster1", "webtop1a": "cluster1a"},
    "user2": {"webtop2": "cluster2", "webtop2a": "cluster2a"},
}