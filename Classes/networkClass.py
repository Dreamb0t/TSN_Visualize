import networkx as nx
import csv

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


                


    def load_streams(self, streamsCSV):
        #TODO
        """ Load streams from CSV and compute shortest paths """
        with open(streamsCSV, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for row in reader:
                stream_name = row[1]
                source_node = self.nodes[row[3]]
                destination_node = self.nodes[row[4]]

                if source_node in self.graph and destination_node in self.graph:
                    try:
                        path = nx.shortest_path(self.graph, source=source_node, target=destination_node)
                    except nx.NetworkXNoPath:
                        path = ["No Path Found"]
                else:
                    path = ["Invalid Nodes"]

                self.streams[stream_name] = Stream(stream_name, source_node, destination_node)
                self.streams[stream_name].path = path
                #print(path)

    def get_stream_path(self, stream_name):
        """ Retrieve the shortest path for a given stream """
        return self.streams.get(stream_name, Stream("", "", "")).path
    