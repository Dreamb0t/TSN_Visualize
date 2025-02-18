class Node:
    def __init__(self, name, node_type):
        self.name = name
        self.type = node_type
        self.in_edges = []   # List to store edges coming into this node.
        self.out_edges = []  # List to store edges leaving this node.

    def add_in_edge(self, edge):
        """Add an incoming edge to this node."""
        self.in_edges.append(edge)

    def add_out_edge(self, edge):
        """Add an outgoing edge from this node."""
        self.out_edges.append(edge)

    def __str__(self):
        return f"{self.name} ({self.type})"