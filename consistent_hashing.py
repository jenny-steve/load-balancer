import math

class ConsistentHashMap:
    def __init__(self, num_containers, num_slots, num_virtual_servers):
        #Initialize parameters

        self.num_containers = num_containers # Initialize No of server containers
        self.num_slots = num_slots # Initialize No of slots in hash map
        self.num_virtual_servers = num_virtual_servers # Initialize No of virtual servers for each container
        self.hash_map = [None] * num_slots 
        self.virtual_servers = {}
        self._initialize_virtual_servers()

    def _initialize_virtual_servers(self):
        # Initialize virtual servers and assign them to slots in the hash map.
        for i in range(self.num_containers):
            self.virtual_servers[i] = []
            for j in range(self.num_virtual_servers):
                slot = self._hash_virtual_server(i, j)
                while self.hash_map[slot] is not None:
                    slot = (slot + 1) % self.num_slots  # Linear probing
                self.hash_map[slot] = (i, j)
                self.virtual_servers[i].append(slot)

    def _hash_virtual_server(self, i, j):
        """
        Hash function for virtual servers.
        :param i: Server container index
        :param j: Virtual server index
        :return: Slot index
        """
        return (i + j**2 + 2*j + 25) % self.num_slots

    def _hash_request(self, request_id):
        return (request_id**2 + 2*request_id + 17) % self.num_slots

    def assign_request(self, request_id):
        slot = self._hash_request(request_id)
        while self.hash_map[slot] is None:
            slot = (slot + 1) % self.num_slots  # Linear probing
        return self.hash_map[slot][0]  # Return the server container ID
