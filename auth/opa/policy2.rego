package envoy.authz

import input.attributes.request.http as http_request

default allow = false

# Extract the current authenticated user from x-current-user header
current_user = user {
    user := http_request.headers["x-current-user"]
}

# Allow access if the URL path matches the user's namespace and the requested service is in the allowed list
allow {
    user := current_user
    path := split(http_request.path, "/")
    namespace := path[1]  # Assumes URL format /<username>/<webtop>

    user == namespace
    webtop_service := path[2]

    # Check if the webtop service is one of the allowed services for the user
    webtop_service == user_webtop_services[user][_]
}

# Define allowed webtop services per user as a list
user_webtop_services = {
    "user1": ["webtop1", "webtop1a", "webtop1b"],
    "user2": ["webtop2", "webtop2a"],
}
