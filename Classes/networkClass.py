import networkx as nx
import csv

from .nodeClass import Node
from .streamClass import Stream


class Network:
    def __init__(self, topologyCsv, streamCsv):
        self.graph = nx.Graph()
        self.nodes = {}  # Store nodes as objects
        self.streams = {}
        self.create_topology(topologyCsv)
        self.load_streams(streamCsv)

    def create_topology(self, topologyCSV):
        """ Define the network topology (Switches & Endstations) """
        with open(topologyCSV, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                type = row[0]
                name = row[1]
                port = row[3]

                #Adds edges
                if row[0] == "LINK":
                    source_node =row[2]
                    destination_node = row[4]
                    self.graph.add_edge(source_node, destination_node)
                
                else:
                    node = Node(name, type, port)  # Create a Node object
                    self.nodes[node.name] = node  # Store Node object
                    self.graph.add_node(node.name, node_obj=node)

                print(node)
                
        # Adding links (Modify as needed)

        # Apply spring layout for better visualization
        pos = nx.spring_layout(self.graph, seed=42, scale=400)  # Adjust scale for spacing
        
        #TODO Make dynamically scaleable, so given a large network, the spacing should be bigger.
        # Store computed positions in the graph with an offset to center them
        for node, (x, y) in pos.items():
            self.graph.nodes[node]["pos"] = (x + 50, y + 50)  # Adjust offsets

    def load_streams(self, streamsCSV):
        #TODO
        """ Load streams from CSV and compute shortest paths """
        with open(streamsCSV, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for row in reader:
                stream_name = row[1]
                source_node = row[3]
                destination_node = row[4]

                if source_node in self.graph and destination_node in self.graph:
                    try:
                        path = nx.shortest_path(self.graph, source=source_node, target=destination_node)
                    except nx.NetworkXNoPath:
                        path = ["No Path Found"]
                else:
                    path = ["Invalid Nodes"]

                self.streams[stream_name] = Stream(stream_name, source_node, destination_node)
                self.streams[stream_name].path = path
                print(path)

    def get_stream_path(self, stream_name):
        """ Retrieve the shortest path for a given stream """
        return self.streams.get(stream_name, Stream("", "", "")).path
    