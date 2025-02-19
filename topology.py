import sys
import csv
import networkx as nx
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QPushButton
from PyQt5.QtGui import QPen, QBrush, QFont
from PyQt5.QtCore import Qt

topologyCSV = "topology.csv"
class Stream:
    def __init__(self, source_node, destination_node):
        pass

class Node:
    def __init__(self, name, type, port):
        self.name = name
        self.type = type
        self.port = port

    def __str__(self):
        return f"{self.name} ({self.type}, Port: {self.port})"

class Network:
    def __init__(self):
        self.graph = nx.Graph()
        self.nodes = {}  # Store nodes as objects
        self.streams = {}
        self.create_topology()

    def create_topology(self):
        """ Define the network topology (Switches & Endstations) """
        with open(topologyCSV, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                type = row[0]
                name = row[1]
                port = row[3]


                if row[0] == "LINK": #TODO add the edges
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

        # Store computed positions in the graph with an offset to center them
        for node, (x, y) in pos.items():
            self.graph.nodes[node]["pos"] = (x + 50, y + 50)  # Adjust offsets

        # Predefine paths (Streams)
        # self.streams = {
        #     "Stream1": ["E1", "S1", "S2", "S3", "E2"],
        #     "Stream2": ["E1", "S1", "S3", "E2"]
        # }

    def get_stream_path(self, stream_name):
        return self.streams.get(stream_name, [])

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node: Node, x, y):
        super().__init__(x - 10, y - 10, 20, 20)  # Circle shape
        self.node = node  # Store the Node instance
        self.setBrush(QBrush(Qt.blue if node.type == "SW" else Qt.green))
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)

        # Create a label for the node
        self.label = QGraphicsTextItem(node.name)
        self.label.setDefaultTextColor(Qt.black)
        self.label.setFont(QFont("Arial", 10))
        self.label.setPos(x-10, y-30)

    def mousePressEvent(self, event):
        print(f"Clicked on: {self.node.name}, Type: {self.node.type}, Port: {self.node.port}")
        window2.show()

class UI(QMainWindow):
    def __init__(self, network):
        super().__init__()
        self.setWindowTitle("Interactive Network Topology")
        self.setGeometry(100, 100, 800, 600)
        self.network = network
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        main_layout = QVBoxLayout(self.centralWidget)

        # Dropdown and button layout
        self.layout = QHBoxLayout()
        self.dropdown = QComboBox()
        self.dropdown.addItems(self.network.streams.keys())
        self.dropdown.currentTextChanged.connect(self.highlight_path)
        self.layout.addWidget(self.dropdown)

        self.button = QPushButton("Display Stream")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.button_was_toggled)
        self.button.clicked.connect(self.button_clicked)

        self.layout.addWidget(self.button)
        main_layout.addLayout(self.layout)

        # Graphics view layout
        self.layout2 = QVBoxLayout()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.layout2.addWidget(self.view)
        main_layout.addLayout(self.layout2)

        self.draw_topology()

    def button_clicked(self):
        print("Button clicked")

    def button_was_toggled(self, checked):
        print("Checked:", checked)

    def draw_topology(self):
        """ Render the network topology """
        self.node_items = {}
        self.edge_items = {}

        # Draw edges
        for edge in self.network.graph.edges:
            node1, node2 = edge
            x1, y1 = self.network.graph.nodes[node1]['pos']
            x2, y2 = self.network.graph.nodes[node2]['pos']
            line = self.scene.addLine(x1, y1, x2, y2, QPen(Qt.black, 2))
            self.edge_items[edge] = line

        # Draw nodes
        for node_name, data in self.network.graph.nodes(data=True):
            if "node_obj" not in data:
                print(f"Warning: Missing node data for {node_name}")  # Debugging
                continue  # Skip this node

            node = data["node_obj"]  # Use the correct key
            x, y = data["pos"]
            node_item = NodeItem(node, x, y)
            self.scene.addItem(node_item)
            self.scene.addItem(node_item.label)
            self.node_items[node_name] = node_item


    def highlight_path(self, selected_stream):
        """ Highlight the selected stream path """
        path = self.network.get_stream_path(selected_stream)

        # Reset colors
        for line in self.edge_items.values():
            line.setPen(QPen(Qt.black, 2))

        # Highlight path
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            if edge in self.edge_items:
                self.edge_items[edge].setPen(QPen(Qt.red, 3))
            elif (edge[1], edge[0]) in self.edge_items:  # Reverse lookup
                self.edge_items[(edge[1], edge[0])].setPen(QPen(Qt.red, 3))

class SecondUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        self.setGeometry(200, 200, 800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    network = Network()
    window = UI(network)
    window.show()
    window2 = SecondUI()
    sys.exit(app.exec_())
