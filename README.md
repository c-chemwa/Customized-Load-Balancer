# Customized-Load-Balancer

Implementation of a load balancer that routes the requests coming from several clients asynchronously among several servers so that the load is nearly evenly distributed among them.

---

## 📌 Task 1: Web Server

This task implements a simple web server using **Python Flask**, containerized with Docker. Each server instance responds with its unique ID and a heartbeat check, which will later be used by the load balancer.

---

### 🚀 Endpoints

| Method | Endpoint      | Description                                           |
|--------|---------------|-------------------------------------------------------|
| GET    | `/home`       | Returns the server's unique ID                       |
| GET    | `/heartbeat`  | Responds with `200 OK` to signal server health       |

Example Response from `/home`:

```json
{
  "message": "Hello from Server: 1",
  "status": "successful"
}
```

---

## ⚙️ Task 2: Consistent Hashing

This task implements a consistent hashing mechanism to evenly distribute client requests among a dynamic set of server replicas.

---

### 🧠 Core Concepts

- The system maintains a **circular hash ring with 512 slots**.
- Each server is represented by **9 virtual replicas** (K = log₂(512)).
- Requests and servers are mapped to slots using custom hash functions:
  - **Request Hash**: `H(i) = 3i + 17`
  - **Virtual Server Hash**: `Φ(i,j) = i + 3j + 25`
- **Linear probing** is used to resolve hash collisions when placing virtual servers.

---

### 📦 Features Implemented

- `add_server(server_id)` – Adds a server with 9 virtual replicas into the hash ring.
- `remove_server(server_id)` – Removes the server and all its associated virtual nodes.
- `get_server_for_key(request_id)` – Returns the correct server based on the hashed request ID.

---

### 🧪 Sample Usage

```python
from consistent_hash import ConsistentHash

ch = ConsistentHash()
ch.add_server(1)
ch.add_server(2)
ch.add_server(3)

for i in range(10):
    server = ch.get_server_for_key(i)
    print(f"Request {i} routed to Server {server}")
```

Sample output:

```
Request 0 routed to Server 2
Request 1 routed to Server 1
Request 2 routed to Server 3
...
```

---

### ✅ Status

- [x] Circular hash ring (512 slots)
- [x] 9 virtual nodes per server
- [x] Custom hash functions for requests and servers
- [x] Collision resolution with linear probing
- [x] Fully tested with request routing simulation

This hashing structure will now be used in Task 3 to implement routing and fault-tolerant request scheduling inside the load balancer.

---
