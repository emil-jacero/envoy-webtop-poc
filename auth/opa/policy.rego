package envoy.authz

import rego.v1

import data.users

default allow := false

default headers := {}

# Function to parse the Basic Auth header and extract the username
basic_auth_user := user if {
	[_, payload] := split(input.attributes.request.http.headers.authorization, " ")
	decoded := base64url.decode(payload)
	[user, _] := split(decoded, ":")
}

allow if {
	user := basic_auth_user
	is_user_valid[user]
}

# Validate user by matching extracted user with the namespace in the path
is_user_valid[user] if {
	user := basic_auth_user
    path := split(input.attributes.request.http.path, "/")
	namespace := path[1] # Assume URL format is /<username>/<resource>
	resource := path[2] # Assume URL format is /<username>/<resource>

	# Ensure the extracted user has an entry in the users object
	# and the namespace from URL matches this user
	users[user] != null
	user == namespace  # Check if the user matches the namespace path
    resource in users[user].clusters  # Check if the resource exists in the cluster list
}

# Add headers if the request is allowed
headers := {"X-Resource-Cluster": resource} if {
	allow
	path := split(input.attributes.request.http.path, "/")
	resource := path[2] # Extract the resource part from the path
}
