from flask import Flask, request, jsonify
from consistent_hashing import ConsistentHashMap
import math

app = Flask(__name__)

# Parameters for consistent hashing
N = 3  # Number of server containers
num_slots = 512  # Total number of slots in the hash map
K = int(math.log2(num_slots))  # Number of virtual servers per container

# Docker container names
server_containers = ["server1", "server2", "nginx"]

# Initialize the consistent hash map
consistent_hash_map = ConsistentHashMap(N, num_slots, K)

@app.route('/home', methods=['GET'])
def home():
    return "Welcome to the Home Page!"

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({"status": "alive"})

@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({
        "message": {
            "N": N,
            "replicas": server_containers
        },
        "status": "successful"
    }), 200

@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.get_json()
    n = data.get('n')
    hostnames = data.get('hostnames')

    if n != len(hostnames):
        return jsonify({
            "message": "<Error> Length of hostname list is more than newly added instances",
            "status": "failure"
        }), 400

    global N
    N += n
    server_containers.extend(hostnames)

    # Reinitialize the consistent hash map with the new server count
    consistent_hash_map = ConsistentHashMap(N, num_slots, K)

    return jsonify({
        "message": {
            "N": N,
            "replicas": server_containers
        },
        "status": "successful"
    }), 200

@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.get_json()
    n = data.get('n')
    hostnames = data.get('hostnames')

    if n != len(hostnames):
        return jsonify({
            "message": "<Error> Length of hostname list is more than removable instances",
            "status": "failure"
        }), 400

    global N
    N -= n
    for hostname in hostnames:
        server_containers.remove(hostname)

    # Reinitialize the consistent hash map with the new server count
    consistent_hash_map = ConsistentHashMap(N, num_slots, K)

    return jsonify({
        "message": {
            "N": N,
            "replicas": server_containers
        },
        "status": "successful"
    }), 200

@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    if path == "home":
        request_id = request.args.get('request_id', type=int)
        server_id = consistent_hash_map.assign_request(request_id)
        # Return the Docker container name
        return f"Request {request_id} routed to {server_containers[server_id]}"
    else:
        return jsonify({
            "message": "<Error> '/other' endpoint does not exist in server replicas",
            "status": "failure"
        }), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
