import math

class ConsistentHashMap:
    def __init__(self, num_containers, num_slots, num_virtual_servers):
        self.num_containers = num_containers
        self.num_slots = num_slots
        self.num_virtual_servers = num_virtual_servers
        self.hash_map = [None] * num_slots
        self.virtual_servers = {}
        self._initialize_virtual_servers()

    def _initialize_virtual_servers(self):
        for i in range(self.num_containers):
            self.virtual_servers[i] = []
            for j in range(self.num_virtual_servers):
                slot = self._hash_virtual_server(i, j)
                while self.hash_map[slot] is not None:
                    slot = (slot + 1) % self.num_slots  # Linear probing
                self.hash_map[slot] = (i, j)
                self.virtual_servers[i].append(slot)

    def _hash_virtual_server(self, i, j):
        return (i + j**2 + 2*j + 25) % self.num_slots

    def _hash_request(self, request_id):
        return (request_id**2 + 2*request_id + 17) % self.num_slots

    def assign_request(self, request_id):
        slot = self._hash_request(request_id)
        while self.hash_map[slot] is None:
            slot = (slot + 1) % self.num_slots  # Linear probing
        return self.hash_map[slot][0]  # Return the server container ID
