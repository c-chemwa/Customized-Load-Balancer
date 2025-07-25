import hashlib

class ConsistentHash:
    def __init__(self, num_slots=2048, virtuals_per_server=100):
        self.num_slots = num_slots
        self.virtuals = virtuals_per_server
        self.hash_ring = {}      # slot → server_id
        self.sorted_slots = []   # ordered slot positions
        self.server_virtuals = {}  # server_id → list of slots

    def _hash_request(self, key):
        h = hashlib.md5(str(key).encode()).hexdigest()
        return int(h, 16) % self.num_slots

    def _hash_virtual(self, server_id, j):
        h = hashlib.md5(f"{server_id}:{j}".encode()).hexdigest()
        return int(h, 16) % self.num_slots

    def add_server(self, server_id):
        self.server_virtuals[server_id] = []
        for j in range(self.virtuals):
            slot = self._hash_virtual(server_id, j)
            original_slot = slot
            while slot in self.hash_ring:
                slot = (slot + 1) % self.num_slots
                if slot == original_slot:
                    raise Exception("Hash ring full")
            self.hash_ring[slot] = server_id
            self.server_virtuals[server_id].append(slot)
        self.sorted_slots = sorted(self.hash_ring.keys())

    def remove_server(self, server_id):
        if server_id not in self.server_virtuals:
            return
        for slot in self.server_virtuals[server_id]:
            self.hash_ring.pop(slot, None)
        self.server_virtuals.pop(server_id)
        self.sorted_slots = sorted(self.hash_ring.keys())

    def get_server_for_key(self, key):
        slot = self._hash_request(key)
        for s in self.sorted_slots:
            if s >= slot:
                return self.hash_ring[s]
        return self.hash_ring[self.sorted_slots[0]] if self.sorted_slots else None
