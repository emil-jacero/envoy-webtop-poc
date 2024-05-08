package envoy.authz

import input.attributes.request.http as http_request

default allow = false

# Extract basic auth username
basic_auth_user = user {
    [_, payload] := split(http_request.headers.authorization, " ")
    [user, _] := split(base64url.decode(payload), ":")
}

# Allow access if the URL path matches the user's namespace and the requested service is in the allowed list
allow {
    user := basic_auth_user
    path := split(http_request.path, "/")
    namespace := path[1]  # Assumes URL format /<username>/<webtop>

    user == namespace
    webtop_service := path[2]

    # Check if the webtop service is one of the allowed services for the user
    webtop_service == user_webtop_services[user][_]
}

# Define allowed webtop services per user as a list
user_webtop_services = {
    "user1": ["webtop1", "webtop1a", "webtop1b"],  # user1 can access webtop1, webtop1a, and webtop1b
    "user2": ["webtop2", "webtop2a"],              # user2 can access webtop2 and webtop2a
    # Add additional users and their list of services here
}
