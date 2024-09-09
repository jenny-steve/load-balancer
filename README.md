# Consistent Hashing Load Balancer
Implementing a load balancer that routes the requests coming from several clients among several servers so that the load is nearly evenly distributed.

## Overview

This project demonstrates a load balancer using consistent hashing to distribute requests across multiple server instances. It uses Flask for the web server and a custom consistent hashing implementation to manage the distribution of requests.

## Prerequisites

Before you start, ensure you have the following installed on your machine:

- **Python 3.8+**: Download and install from [Python's official website](https://www.python.org/downloads/).
- **Docker**: Download and install Docker from [Docker's official website](https://www.docker.com/products/docker-desktop).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/load-balancer.git
   cd load-balancer


2. **Set Up a Virtual Environment**:

   Create a virtual environment in the project directory:

   ```bash
   python3 -m venv venv
   
3. **Activate the virtual environment**:

On Windows:
   ```bash
   **Copy code**:
   venv\Scripts\activate
On macOS/Linux:
   ```bash
   Copy code
   source venv/bin/activate
Install Dependencies:

Install the required Python libraries using pip:

bash
Copy code
pip install -r requirements.txt
Build and Run Docker Containers:

Ensure Docker is running.

Navigate to the directory containing your Dockerfile.

Build the Docker images:

bash
Copy code
docker build -t server1 ./server1
docker build -t server2 ./server2
docker build -t nginx ./nginx
Run the Docker containers:

bash
Copy code
docker network create lb_network
docker run -d --name server1 --net lb_network server1
docker run -d --name server2 --net lb_network server2
docker run -d -p 80:80 --name nginx --net lb_network nginx
Project Structure
plaintext
Copy code
├── consistent_hashing.py      # Contains the ConsistentHashMap class
├── DS_Task.py                 # Main Flask application that runs the load balancer
├── Dockerfile                 # Dockerfile for building the server images
├── nginx.conf                 # Configuration file for NGINX load balancer
├── requirements.txt           # Python dependencies
└── README.md                  # This file
Usage
Start the Flask Application:

The Flask application is responsible for handling the incoming requests and routing them to the appropriate server using the consistent hashing algorithm.

bash
Copy code
python DS_Task.py
The application will start on http://localhost:5000.

Interacting with the Load Balancer:

Check Home Page: Access http://localhost:80/home to check if the load balancer is running.
Check Heartbeat: Access http://localhost:80/heartbeat to check if the servers are alive.
Add New Server Instances: You can add more server instances to the load balancer by sending a POST request to http://localhost:80/add with the following JSON data:
json
Copy code
{
  "n": 1,
  "hostnames": ["Server 4"]
}
The load balancer will then distribute requests to this new server.
Remove Server Instances: You can remove server instances by sending a DELETE request to http://localhost:80/rm with the following JSON data:
json
Copy code
{
  "n": 1,
  "hostnames": ["Server 1"]
}
Assign Requests: To route a request based on consistent hashing, access http://localhost:80/{path}?request_id={id}, where path is the desired endpoint and id is the unique request ID.
NGINX Configuration:

The NGINX configuration file nginx.conf specifies the upstream servers and routes incoming requests to the correct backend server.

Example NGINX configuration:

nginx
Copy code
events {}

http {
    upstream myapp {
        server server1:5000;
        server server2:5000;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://myapp;
        }

        error_page 404 500 502 503 504 /50x.html;
        location = /50x.html {
            root /usr/share/nginx/html;
        }
    }
}
Debugging
If you encounter issues while running the project, here are some steps to debug:

Check Docker Logs:

Run the following command to view the logs of any Docker container:

bash
Copy code
docker logs <container_name>
For example:

bash
Copy code
docker logs nginx
Check Flask Application Logs:

Ensure that your Flask application is running without errors. You can view the logs in the terminal where the Flask application is running.

Test Individual Endpoints:

Use tools like Postman or curl to test the individual endpoints and see if the responses are as expected.

Network Issues:

Ensure that all your Docker containers are on the same network (lb_network in this case) and can communicate with each other.

Check Consistent Hashing Logic:

If requests are not being routed correctly, review the consistent_hashing.py file to ensure the hashing and slot assignment logic is functioning correctly.