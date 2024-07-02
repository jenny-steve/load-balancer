from flask import Flask, jsonify
from consistent_hashing import ConsistentHashMap  # Import the ConsistentHashMap class
import math
import os

app = Flask(__name__)

# Parameters for consistent hashing
N = 3
num_slots = 512
K = int(math.log2(num_slots))

# Initializing the consistent hash map
consistent_hash_map = ConsistentHashMap(N, num_slots, K)

# Defining application route
@app.route('/home')
def home():
    return jsonify({"message": "Welcome to the home page! We are glad to have you here."})

@app.route('/heartbeat')
def heartbeat():
    return jsonify({"status": "alive"})

@app.route('/assign/<int:request_id>')
def assign(request_id):
    server_id = consistent_hash_map.assign_request(request_id)
    return jsonify({"request_id": request_id, "assigned_server": server_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
