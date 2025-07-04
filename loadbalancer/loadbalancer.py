from flask import Flask, jsonify, request, abort
import os
import random
import string
from consistent_hash import ConsistentHash

app = Flask(__name__)
ch = ConsistentHash()
N = 3  # Default number of servers

# Initialize with 3 servers
for i in range(1, N + 1):
    ch.add_server(i)

def generate_random_hostname(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

# Simulate spawning a server (no actual Docker command)
def spawn_server(server_id):
    print(f"Simulating spawn of Server {server_id} with hostname {generate_random_hostname()}")
    ch.add_server(server_id)

# Simulate removing a server (no actual Docker command)
def remove_server(server_id):
    print(f"Simulating removal of Server {server_id}")
    ch.remove_server(server_id)

# Endpoint to get replica status
@app.route('/rep', methods=['GET'])
def get_replicas():
    replicas = [f"Server {i}" for i in range(1, N + 1)]
    return jsonify({
        "message": {
            "N": N,
            "replicas": replicas,
            "status": "successful"
        }
    }), 200

# Endpoint to add new server instances
@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.get_json()
    if not data or 'n' not in data:
        abort(400)
    new_n = data['n']
    hostnames = data.get('hostnames', [])
    if len(hostnames) > new_n:
        return jsonify({
            "message": "Error: Length of hostname list is more than newly added instances",
            "status": "failure"
        }), 400
    global N
    N += new_n
    for i in range(N - new_n + 1, N + 1):
        spawn_server(i)
    return jsonify({
        "message": {
            "N": N,
            "replicas": [f"Server {i}" for i in range(1, N + 1)],
            "status": "successful"
        }
    }), 200

# Endpoint to remove server instances
@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.get_json()
    if not data or 'n' not in data:
        abort(400)
    remove_n = data['n']
    hostnames = data.get('hostnames', [])
    if len(hostnames) > remove_n:
        return jsonify({
            "message": "Error: Length of hostname list is more than removable instances",
            "status": "failure"
        }), 400
    global N
    if N - remove_n < 1:
        abort(400)
    N -= remove_n
    for _ in range(remove_n):
        server_id = N + 1  # Remove the last added server for simplicity
        remove_server(server_id)
    return jsonify({
        "message": {
            "N": N,
            "replicas": [f"Server {i}" for i in range(1, N + 1)],
            "status": "successful"
        }
    }), 200

# Endpoint to route requests
@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    if path == 'home':
        key = hash(request.remote_addr or str(random.random())) % 1000  # Simulate client IP
        server_id = ch.get_server_for_key(key)
        if server_id:
            return jsonify({
                "message": f"Hello from Server: {server_id}",
                "status": "successful"
            }), 200
    return jsonify({
        "message": f"Error: /{path} endpoint does not exist in server replicas",
        "status": "failure"
    }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
