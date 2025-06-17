# Customized-Load-Balancer
Implementation of a load balancer that routes the requests coming from several clients asynchronously among several servers so that the load is nearly evenly distributed among them.

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

