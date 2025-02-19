import networkx as nx
import csv
from datetime import datetime
from networkx import shortest_path

from .nodeClass import Node, Switch, EndStation
from .streamClass import Stream
from enums.deviceEnums import NodeType

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
                if type == NodeType.LINK.value:
                    source_node_name = row[2]
                    source_port = row[3]
                    if source_node_name not in self.nodes:
                        if source_node_name.startswith(NodeType.SWITCH.value):
                            source_node = Switch(source_node_name, source_port)
                            self.nodes[source_node_name] = source_node
                            print("LINKING NODE")
                        else:
                            source_node = EndStation(source_node_name, source_port)
                            print("LINKING NODE")
                    destination_node_name = row[4]
                    destination_node_port = row[5]
                    if destination_node_name not in self.nodes:
                        if destination_node_name.startswith(NodeType.SWITCH.value):
                            destination_node = Switch(destination_node_name,destination_node_port)
                            self.nodes[destination_node_name] = destination_node
                            print("LINKING NODE")
                        else:
                            destination_node = EndStation(destination_node_name,destination_node_port)
                            print("LINKING NODE")
                            self.nodes[destination_node_name] = destination_node
                    test1 = self.nodes[source_node_name]
                    test2 = self.nodes[destination_node_name]
                    self.graph.add_edge(test1, test2)
                    #print(self.graph.edges)
                elif type == NodeType.SWITCH.value:
                    name = row[1]
                    port = row[3]
                    switch = Switch(name, port)
                    self.nodes[switch.name] = switch
                    self.graph.add_node(switch.name, node_obj=switch)
                    print(switch)
                elif type == NodeType.ENDSTATION.value:
                    name = row[1]
                    port = row[3]
                    es = EndStation(name, port)
                    self.nodes[es.name] = es
                    self.graph.add_node(es.name, node_obj=es)
                    print(es)

    def shortestPath(self, stream: Stream):
            # Get the names of the source and destination from the stream.
            source_name = stream.source_node.name
            destination_name = stream.destination_node.name

            # Check that both nodes exist in the graph.
            if source_name in self.graph and destination_name in self.graph:
                try:
                    # Compute the shortest path using NetworkX.
                    path = nx.shortest_path(self.graph, source=stream.source_node, target=stream.destination_node)
                except nx.NetworkXNoPath:
                    path = ["No Path Found"]
            else:
                path = ["Invalid Nodes"]

            #store a small data package in the destination
            self.nodes[destination_name].arrivals.append({
                        "source node name": stream.source_node,   # Reference to the stream
                        #"path": path,
                        "data size": stream.size,       # The computed path
                        "arrival_time":  datetime.now() # Optionally, compute an arrival time here
                    })
            self.streams[stream.stream_name].path = path
            self.trafficSwitches(stream.stream_name)

    def trafficSwitches(self, stream_id):
        """
        Given a path, for each switch node in the path,
        add the immediately preceding node to that switch's traffic.
        """
        stream = self.streams[stream_id]
        path = stream.path
        # Start from index 1 because the first node (index 0) doesn't have a previous node and is anlways an endstation.
        for i in range(1, len(path)):
            current_node = path[i]
            # Check if current node is a switch.
            if current_node.type == NodeType.SWITCH:
                previous_node = path[i-1]
                current_node.add_traffic(stream_id, previous_node, stream.size, stream.deadline)

                

    def load_streams(self, streamsCSV):
        #TODO
        """ Load streams from CSV and compute shortest paths """
        with open(streamsCSV, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for row in reader:
                pcp = row[0]
                stream_name = row[1]
                stream_type = row[2]

                source_node_name = row[3]
                source_node = self.nodes[source_node_name]

                destination_node_name = row[4]
                destination_node = self.nodes[destination_node_name]

                size = row[5]
                period = row[6]
                deadline = row[7]

                s = Stream(pcp, stream_name, stream_type, source_node, destination_node, size, period, deadline)
                self.streams[stream_name] = s
                self.shortestPath(s)

    

    def get_stream_path(self, stream_name):
        """ Retrieve the shortest path for a given stream """
        path = self.streams.get(stream_name).path
        print(path)
        print(path[0])
        lastnode = path[-1]
        print(lastnode)
        return path
    