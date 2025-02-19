from node import *
class Stream:
    """
    Represents a network stream with the following properties:
    
    Attributes:
        pcp (int): Priority Code Point value (0-7) indicating the stream's priority.
        stream_name (str): Unique identifier for the stream.
        stream_type (str): Shorthand for the stream type (e.g., 'ST' for Scheduled Traffic, 'AVB' for Audio Video Bridging).
        source_node (Node): Identifier of the source node (end system) of the stream.
        destination_node (Node): Identifier of the destination node (end system) of the stream.
        size (int): Size of the stream's packets in bytes.
        period (int): Period of the stream (in units specified in the configuration file).
        deadline (int): Deadline of the stream (in units specified in the configuration file).
    """
    def __init__(self, pcp, stream_name, stream_type, source_node:EndStation, destination_node:EndStation, size, period, deadline):
        self.pcp = int(pcp)  # Ensuring PCP is stored as an integer.
        self.stream_name = stream_name
        self.stream_type = stream_type
        self.source_node = source_node
        self.destination_node = destination_node
        self.size = int(size)
        self.period = int(period)
        self.deadline = int(deadline)

    def __repr__(self):
        return (f"Stream(pcp={self.pcp}, stream_name='{self.stream_name}', stream_type='{self.stream_type}', "
                f"source_node='{self.source_node.name}', destination_node='{self.destination_node.name}', "
                f"size={self.size}, period={self.period}, deadline={self.deadline})")
