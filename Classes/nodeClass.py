from enums.deviceEnums import NodeType

class Node:
    def __init__(self, name, type, port):
        self.name = name
        self.type = type
        self.port = port

    def __repr__(self):
        return self.name
    
    def __str__(self):
        return f"{self.name} ({self.type}, Port: {self.port})"
    
class EndStation(Node):
    def __init__(self, name, port):
        super().__init__(name, NodeType.ENDSTATION, port)
        self.arrivals = []


    def __str__(self):
        arrival_info = ", ".join(
            f"{rec['source node name']} -> {rec['data size']} at {rec['arrival_time']}"
            for rec in self.arrivals
        )
        return f"{self.name} ({self.type}), Arrivals: [{arrival_info}]"


class Switch(Node):
    def __init__(self, name, port):
        super().__init__(name, NodeType.SWITCH, port)
        self.traffic = {}  # Dictionary mapping stream id -> { 'previous_node': Node, 'data_size': value, 'time': value }
       #self.sent_packages = []  

    def add_traffic(self, stream_id, previous_node, data_size, time):
        """
        Records traffic information for a given stream.
        
        Args:
            stream_id (str): The identifier of the stream.
            previous_node (Node): The node immediately preceding this switch for that stream.
            data_size: The size of the data (could be an int, float, etc.).
            time: The time at which the data was sent/received.
        """
        self.traffic[stream_id] = {
            'previous_node': previous_node,
            'data_size': data_size,
            'time': time
        }

    def __str__(self):
        # For a switch, if it has a preceding node (set via set_preceding_node), display it.
        preceding = self.preceding_node.name if hasattr(self, 'preceding_node') and self.preceding_node else "None"
        # Build a string representing the traffic dictionary.
        traffic_info = ", ".join(
            f"{stream_id}: from {info['previous_node'].name if info['previous_node'] else 'None'} "
            f"(size: {info['data_size']}, time: {info['time']})"
            for stream_id, info in self.traffic.items()
        )
        return f"{self.name} ({self.type}), Preceding: {preceding}, Traffic: [{traffic_info}]"
