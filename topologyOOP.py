import sys
import csv
import networkx as nx
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsScene, QGraphicsView, 
                             QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, 
                             QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton)
from PyQt5.QtGui import QPen, QBrush, QFont
from PyQt5.QtCore import Qt
from enums import NodeType  # Ensure your enums.py defines NodeType with SWITCH, ENDSTATION, and LINK

# Base Node classes (can be expanded as needed)




class Network:
    def __init__(self):
        # Use a directed graph; for an undirected topology, change to nx.Graph()
        self.graph = nx.DiGraph()
        # Dictionaries to store node data for later use (e.g., visualization)
        self.switches = {}    # keys: node names, values: node properties
        self.endstations = {} # keys: node names, values: node properties

    def create_topology_from_csv(self, csv_file):
        with open(csv_file, newline='') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                # Expected CSV row format: [type, name, source, int, target, int, int]
                try:
                    row_type = row[0].strip()
                    name     = row[1].strip()
                    source   = row[2].strip()
                    value1   = row[3].strip()  # Convert to int if needed
                    target   = row[4].strip()
                    value2   = row[5].strip()
                    value3   = row[6].strip()
                except Exception as e:
                    print("Error parsing row:", row, e)
                    continue

                # Handle node definitions.
                if row_type == NodeType.SWITCH.value:
                    if name not in self.switches:
                        self.switches[name] = {
                            "name": name,
                            "source": source,
                            "value1": value1,
                            "target": target,
                            "value2": value2,
                            "value3": value3
                        }
                    if name not in self.graph:
                        self.graph.add_node(name, type=NodeType.SWITCH.value)
                elif row_type == NodeType.ENDSTATION.value:
                    if name not in self.endstations:
                        self.endstations[name] = {
                            "name": name,
                            "source": source,
                            "value1": value1,
                            "target": target,
                            "value2": value2,
                            "value3": value3
                        }
                    if name not in self.graph:
                        self.graph.add_node(name, type=NodeType.ENDSTATION.value)
                elif row_type == NodeType.LINK.value:
                    # For a link row, use the source and target fields.
                    if source not in self.graph:
                        if source.startswith(NodeType.SWITCH.value):
                            self.graph.add_node(source, type=NodeType.SWITCH.value)
                        else:
                            self.graph.add_node(source, type=NodeType.ENDSTATION.value)
                    if target not in self.graph:
                        if target.startswith(NodeType.SWITCH.value):
                            self.graph.add_node(target, type=NodeType.SWITCH.value)
                        else:
                            self.graph.add_node(target, type=NodeType.ENDSTATION.value)
                    self.graph.add_edge(source, target,
                                        name=name,
                                        value1=value1,
                                        value2=value2,
                                        value3=value3)
                else:
                    print(f"Unknown row type: {row_type}")

        # Compute node positions using a spring layout (adjust scaling as needed)
        pos = nx.spring_layout(self.graph)
        for node, p in pos.items():
            x = p[0] * 500 + 400
            y = p[1] * 500 + 300
            self.graph.nodes[node]['pos'] = (x, y)

# Custom QGraphicsEllipseItem to display a node.
class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node_name, node_type, x, y):
        super().__init__(x - 10, y - 10, 20, 20)  # Draw a circle centered at (x, y)
        self.node_name = node_name
        self.node_type = node_type
        # Color: blue for switches, green for endstations.
        color = Qt.blue if node_type == NodeType.SWITCH.value else Qt.green
        self.setBrush(QBrush(color))
        self.setPen(QPen(Qt.black, 1))
        # Add a text label.
        self.label = QGraphicsTextItem(node_name)
        self.label.setFont(QFont("Arial", 10))
        self.label.setDefaultTextColor(Qt.black)
        self.label.setPos(x - 10, y - 30)

# Main UI class for displaying the network topology.
class UI(QMainWindow):
    def __init__(self, network):
        super().__init__()
        self.setWindowTitle("Network Topology")
        self.setGeometry(100, 100, 900, 700)
        self.network = network
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        
        # Horizontal layout for input fields and buttons.
        input_layout = QHBoxLayout()
        # For shortest path.
        self.source_line = QLineEdit()
        self.source_line.setPlaceholderText("Enter source node")
        self.target_line = QLineEdit()
        self.target_line.setPlaceholderText("Enter target node")
        self.find_path_btn = QPushButton("Find Shortest Path")
        self.find_path_btn.clicked.connect(self.highlight_shortest_path)
        input_layout.addWidget(self.source_line)
        input_layout.addWidget(self.target_line)
        input_layout.addWidget(self.find_path_btn)
        
        # For constructing a tree from a source node.
        self.tree_source_line = QLineEdit()
        self.tree_source_line.setPlaceholderText("Enter source for tree")
        self.construct_tree_btn = QPushButton("Construct Tree")
        self.construct_tree_btn.clicked.connect(self.highlight_tree)
        input_layout.addWidget(self.tree_source_line)
        input_layout.addWidget(self.construct_tree_btn)
        
        main_layout.addLayout(input_layout)
        
        # Graphics scene and view.
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        main_layout.addWidget(self.view)
        
        self.draw_topology()

    def draw_topology(self):
        self.node_items = {}
        self.edge_items = {}
        # Draw edges first so nodes appear on top.
        for edge in self.network.graph.edges(data=True):
            node1, node2, attr = edge
            x1, y1 = self.network.graph.nodes[node1]['pos']
            x2, y2 = self.network.graph.nodes[node2]['pos']
            line = self.scene.addLine(x1, y1, x2, y2, QPen(Qt.black, 2))
            self.edge_items[(node1, node2)] = line
        # Draw nodes.
        for node, data in self.network.graph.nodes(data=True):
            x, y = data['pos']
            node_item = NodeItem(node, data['type'], x, y)
            self.scene.addItem(node_item)
            self.scene.addItem(node_item.label)
            self.node_items[node] = node_item

    def highlight_shortest_path(self):
        source = self.source_line.text().strip()
        target = self.target_line.text().strip()
        if not source or not target:
            print("Please enter both source and target nodes.")
            return
        
        # Reset all edges to default color (black).
        for line in self.edge_items.values():
            line.setPen(QPen(Qt.black, 2))
        
        try:
            # Compute the shortest path using NetworkX.
            path = nx.shortest_path(self.network.graph, source, target)
            print("Shortest path:", path)
            # Highlight each edge along the shortest path.
            for i in range(len(path) - 1):
                edge = (path[i], path[i+1])
                if edge in self.edge_items:
                    self.edge_items[edge].setPen(QPen(Qt.red, 3))
                elif (edge[1], edge[0]) in self.edge_items:
                    self.edge_items[(edge[1], edge[0])].setPen(QPen(Qt.red, 3))
        except nx.NetworkXNoPath:
            print(f"No path found from {source} to {target}.")
        except Exception as e:
            print("Error computing shortest path:", e)

    def highlight_tree(self):
        source = self.tree_source_line.text().strip()
        if not source:
            print("Please enter a source node for the tree.")
            return
        try:
            # Build a BFS tree from the source node.
            tree_graph = nx.bfs_tree(self.network.graph, source)
            print("Tree nodes:", list(tree_graph.nodes()))
            # Reset all edges.
            for line in self.edge_items.values():
                line.setPen(QPen(Qt.black, 2))
            # Highlight all edges in the tree in red.
            for edge in tree_graph.edges():
                if edge in self.edge_items:
                    self.edge_items[edge].setPen(QPen(Qt.red, 3))
                elif (edge[1], edge[0]) in self.edge_items:
                    self.edge_items[(edge[1], edge[0])].setPen(QPen(Qt.red, 3))
        except Exception as e:
            print("Error constructing tree:", e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    network = Network()
    csv_file_path = "topology.csv"  # Replace with your actual CSV file path
    network.create_topology_from_csv(csv_file_path)
    
    # Debug prints.
    print("Switches:", network.switches)
    print("EndStations:", network.endstations)
    print("Nodes in graph:", list(network.graph.nodes(data=True)))
    print("Edges in graph:", list(network.graph.edges(data=True)))
    
    window = UI(network)
    window.show()
    sys.exit(app.exec_())
