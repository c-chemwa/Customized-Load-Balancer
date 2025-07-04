import random
from loadbalancer.consistent_hash import ConsistentHash  

def simulate_requests(n_requests, n_servers):
    request_counts = {i: 0 for i in range(1, n_servers + 1)}
    ch = ConsistentHash()  # Reset consistent hash for each test
    for i in range(1, n_servers + 1):
        ch.add_server(i)
    for _ in range(n_requests):
        key = random.randint(0, 1000)
        server_id = ch.get_server_for_key(key)
        if server_id:
            request_counts[server_id] += 1
    return request_counts

# A-1: 10000 requests on N=3
n_requests = 10000
n_servers = 3
counts_a1 = simulate_requests(n_requests, n_servers)
print("A-1 Results:", counts_a1)

# A-2: Increment N from 2 to 6
avg_loads_a2 = []
for n in range(2, 7):
    counts = simulate_requests(n_requests, n)
    avg_load = sum(counts.values()) / n
    avg_loads_a2.append(avg_load)
print("A-2 Results:", avg_loads_a2)

# A-3: Simulate failure and recovery
def simulate_failure_recovery(n_servers):
    ch = ConsistentHash()
    for i in range(1, n_servers + 1):
        ch.add_server(i)
    initial_servers = list(ch.server_virtuals.keys())
    ch.remove_server(2)  # Simulate failure of Server 2
    ch.add_server(n_servers + 1)  # Simulate spawning a new server
    return list(ch.server_virtuals.keys())

n_servers_a3 = 3
recovered_servers_a3 = simulate_failure_recovery(n_servers_a3)
print("A-3 Results:", recovered_servers_a3)

# A-4: Modify hash functions
class ModifiedConsistentHash(ConsistentHash):
    def _hash_request(self, i):
        return (5 * i + 13) % self.num_slots
    def _hash_virtual(self, server_id, j):
        return (server_id + 5 * j + 17) % self.num_slots

mod_ch = ModifiedConsistentHash()
for i in range(1, 4):
    mod_ch.add_server(i)
counts_a4 = simulate_requests(n_requests, 3)
print("A-4 Modified Results:", counts_a4)

