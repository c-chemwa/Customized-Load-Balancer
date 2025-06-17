from consistent_hash import ConsistentHash

ch = ConsistentHash()

# Add servers 1, 2, 3
ch.add_server(1)
ch.add_server(2)
ch.add_server(3)

# Simulate 20 request IDs and see how they map
for i in range(20):
    server = ch.get_server_for_key(i)
    print(f"Request ID {i} routed to Server {server}")
