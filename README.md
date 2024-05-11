# envoy-webtop-poc
A Proof-of-Concept for using envoy to authorize webtop instances

## Project Overview

This project is designed to demonstrate a setup involving multiple services with Envoy as a proxy server managing routing and external authorization for these services. The architecture includes an Envoy proxy that delegates authentication and authorization tasks to two separate services: a basic HTTP authentication service and an Open Policy Agent (OPA) service for more complex policy-based authorization. The setup also features two instances of a web-based desktop environment (Webtop), each accessible to different user credentials.

### Services Description

- **Envoy Proxy**: Acts as the front door for all requests, routing them to the appropriate backend service based on the request path, and handles external authorization with two distinct services.
- **ext_authz-http-service**: A simple Flask app that authenticates users using HTTP Basic Authentication against a JSON database of user credentials.
- **ext_authz-opa-service**: Utilizes OPA to perform policy-based authorization checks, particularly deciding if a user should access specific services based on the URL path.
- **webtop1 and webtop2**: Web-based desktop environments that are personalized for two different users. They allow for isolated desktop sessions within the browser, linked to specific user credentials.

### Running the Project

1. **Pre-requisites**:
   - Docker and Docker Compose installed on your system.
   - Ensure ports used in the configuration (10000, 9001, 5000, 9898, 10001, 10002) are free or adjust them in the Docker Compose file if necessary.

2. **Set up configuration files**:
   - Ensure the `envoy.yaml`, `data.json`, and `policy.rego` files are properly set up as per the paths specified in the Docker Compose file.

3. **Build and Run the Docker Compose**:
   - Navigate to the directory containing your `docker-compose.yml`.
   - Run the following command to build and start all the services defined in your Docker Compose file:

     ```bash
     docker-compose up --build -d
     ```

   - This command will pull necessary Docker images, build services defined with a Dockerfile, and start all the services connected via a defined network.

4. **Accessing the Services**:
   - **Envoy Admin Interface**: Accessible at `http://localhost:9001` to monitor the Envoy proxy.
   - **Webtop1 and Webtop2**: Accessible at `http://localhost:10000/user1/webtop1/` and `http://localhost:10000/user2/webtop2/` respectively, each requiring user-specific credentials for access.
   - **Podinfo**: A simple application providing system information, accessible at `http://localhost:10000/` and `http://localhost:10000/podinfo/`.

5. **Monitoring and Logs**:
   - Docker Compose will log output from all containers to the console. You can inspect these logs to monitor the activity and debug issues.

6. **Stopping the Project**:
   - To stop all services and clean up, you can use the following command:

     ```bash
     docker-compose down
     ```

This setup is ideal for environments requiring flexible routing and secure, policy-driven access controls, demonstrating a scalable pattern for managing microservices and externalized authorization in a Dockerized environment.
