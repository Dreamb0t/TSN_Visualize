from enums import NodeType

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

class EndStation(Node):
    def __init__(self, name):
        super().__init__(name, NodeType.ENDSTATION)
        # List to store arrival events.
        # Each event is a dict with keys: 'source', 'target', and 'arrival_time'
        self.arrivals = []

    def add_arrival_info(self, source_node, arrival_time):
        """
        Records an arrival event.
        
        Args:
            source_node: The node (or its identifier) from which an arrival originates.
            arrival_time: The time at which the arrival occurs.
        """
        self.arrivals.append({
            'source': source_node,
            'target': self.name,
            'arrival_time': arrival_time
        })

    def __str__(self):
        # Format arrival info for printing.
        arrival_info = ", ".join(
            f"{rec['source']} -> {rec['target']} at {rec['arrival_time']}" 
            for rec in self.arrivals
        )
        return f"{self.name} ({self.type}), Arrivals: [{arrival_info}]"

class Switch(Node):
    def __init__(self, name):
        super().__init__(name, NodeType.SWITCH)
        # Reference to the node immediately preceding this switch.
        self.preceding_node = None  
        # List to store package send events.
        # Each event is a dict with keys: 'source', 'send_time', and 'package_size'
        self.sent_packages = []

    def set_preceding_node(self, node):
        """
        Sets the node that is immediately before this switch.
        
        Args:
            node: A Node object representing the preceding node.
        """
        self.preceding_node = node

    def add_send_info(self, source_node, send_time, package_size):
        """
        Records a package sent event.
        
        Args:
            source_node: The node (or its identifier) that sent the package.
            send_time: The time the package was sent.
            package_size: The size of the package.
        """
        self.sent_packages.append({
            'source': source_node,
            'send_time': send_time,
            'package_size': package_size
        })

    def __str__(self):
        # Format sent package info for printing.
        package_info = ", ".join(
            f"{rec['source']} at {rec['send_time']} (size: {rec['package_size']})" 
            for rec in self.sent_packages
        )
        preceding = self.preceding_node.name if self.preceding_node else "None"
        return f"{self.name} ({self.type}), Preceding: {preceding}, Sent Packages: [{package_info}]"