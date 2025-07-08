import random
import os
import matplotlib.pyplot as plt
from loadbalancer.consistent_hash import ConsistentHash
from collections import defaultdict
import hashlib


# Make sure output folder exists
os.makedirs("visualizations", exist_ok=True)

ConsistentHash._hash_request = lambda self, i: hash(str(i)) % self.num_slots

def simulate_requests(n_requests, n_servers, ch_class=ConsistentHash):
    request_counts = defaultdict(int)
    ch = ch_class()
    for i in range(1, n_servers + 1):
        ch.add_server(i)

    for _ in range(n_requests):
        key = random.randint(0, 1000)
        server_id = ch.get_server_for_key(key)
        if server_id is not None:
            request_counts[server_id] += 1

    return dict(request_counts)

def plot_bar_chart(data, title, filename, xlabel="Server ID", ylabel="Number of Requests"):
    server_ids = list(data.keys())
    request_counts = list(data.values())
    
    plt.figure(figsize=(8, 5))
    plt.bar(server_ids, request_counts, color='skyblue', edgecolor='black')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(server_ids)
    plt.tight_layout()
    plt.savefig(f"visualizations/{filename}")
    plt.close()

def plot_line_chart(x_vals, y_vals, title, filename, xlabel="Number of Servers", ylabel="Average Load"):
    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, marker='o', color='green')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"visualizations/{filename}")
    plt.close()

#A-1: Base 3-server test

n_requests = 10000
n_servers = 3
counts_a1 = simulate_requests(n_requests, n_servers)
print("A-1 Results:", counts_a1)
plot_bar_chart(counts_a1, "A-1: Request Distribution (3 Servers)", "a1_distribution.png")

#A-2: Vary N from 2 to 6

avg_loads_a2 = []
server_counts = list(range(2, 7))
for n in server_counts:
    counts = simulate_requests(n_requests, n)
    avg_load = sum(counts.values()) / n
    avg_loads_a2.append(avg_load)

print("A-2 Results:", avg_loads_a2)
plot_line_chart(server_counts, avg_loads_a2, "A-2: Avg Load vs Number of Servers", "a2_avg_loads.png")

#A-3: Failure and Recovery

def simulate_failure_recovery(n_servers):
    ch = ConsistentHash()
    for i in range(1, n_servers + 1):
        ch.add_server(i)
    ch.remove_server(2)  # simulate failure
    ch.add_server(n_servers + 1)  # simulate new server
    return list(ch.server_virtuals.keys())

n_servers_a3 = 3
recovered_servers_a3 = simulate_failure_recovery(n_servers_a3)
print("A-3 Results:", recovered_servers_a3)

# Plotting just a bar to show current servers (logical visualization)
a3_result = {sid: 1 for sid in recovered_servers_a3}
plot_bar_chart(a3_result, "A-3: Servers After Failure + Recovery", "a3_failure_recovery.png", ylabel="Active Status")

#A-4: Modified Hash Functions

class ModifiedConsistentHash(ConsistentHash):
    def _hash_request(self, i):
        h = hashlib.sha256(str(i).encode()).hexdigest()
        return int(h, 16) % self.num_slots

    def _hash_virtual(self, server_id, j):
        h = hashlib.sha256(f"{server_id}-{j}".encode()).hexdigest()
        return int(h, 16) % self.num_slots

mod_counts_a4 = simulate_requests(n_requests, 3, ModifiedConsistentHash)
print("A-4 Modified Results:", mod_counts_a4)
plot_bar_chart(mod_counts_a4, "A-4: Request Distribution (Modified Hash)", "a4_modified_hash.png")
