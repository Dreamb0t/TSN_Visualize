from enums.deviceEnums import NodeType

class Node:
    def __init__(self, name, type, port):
        self.name = name
        self.type = type
        self.port = port

    def __str__(self):
        return f"{self.name} ({self.type}, Port: {self.port})"
    
class EndStation(Node):
    def __init__(self, name):
        super().__init__(name, NodeType.ENDSTATION)



    def __str__(self):
        arrival_info = ", ".join(
            f"{rec['source']} -> {rec['target']} at {rec['arrival_time']}" 
            for rec in self.arrivals
        )
        return f"{self.name} ({self.type}), Arrivals: [{arrival_info}]"

# Switch class extends Node and stores a reference to the preceding node and package send info.
class Switch(Node):
    def __init__(self, name):
        super().__init__(name, NodeType.SWITCH)
        self.preceding_node = None  # Reference to the node immediately before this switch.
        self.sent_packages = []     # List of package send events.

    

    def __str__(self):
        preceding = self.preceding_node.name if self.preceding_node else "None"
        package_info = ", ".join(
            f"{rec['source']} at {rec['send_time']} (size: {rec['package_size']})"
            for rec in self.sent_packages
        )
        return f"{self.name} ({self.type}), Preceding: {preceding}, Sent Packages: [{package_info}]"
