import sys
import csv
import networkx as nx
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem,QGraphicsTextItem, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QPushButton
from PyQt5.QtGui import QPen, QBrush, QFont
from PyQt5.QtCore import Qt

topologyCSV = "topology_test.csv"

#Node class to encapsulate switches and end statsion. Idea is this is the parent for when we need to distinguish
#between the child classes Paul Pop's format (PP) and Comcores'(CC) nodes.
class Node:
    def __init__(self,name,type, port):
        self.name = name
        self.type = type
        self.port = port

    #To give a quick summation of what the object contains also
    def __str__(self):
        return f"{self.name} is a {self.type}"

#TODO see if making chil classes is even necessary
# class PPNode(Node):
#     # We give the child Node the class attribute "format" to distinguish between formats. This should be the same
#     #for all nodes that come from a PP file.
#     format = "PPNode"
#     def __init__(self, name, type,extra):
#         super().__init__(name, type)
#         self.extra = extra

#     #includes the format
#     def __str__(self):
#         return super().__str__() + ", format is of " + f"{self.format}"

#TODO this needs to be move to another file once the general structure is in place to make the code look better.

class Network:
    def __init__(self):
        """ Initialize the network graph and its topology """
        self.graph = nx.Graph()
        self.streams = {}
        self.create_topology()

    def create_topology(self):
        """ Define the network topology (Switches & Endstations) """
        node_list = []
        #TODO make a guide, that tells the user, the csv file should be called something specific 
        #(maybe also have a dedicated path) in the folder
        with open(topologyCSV, "r") as f:
            reader = csv.reader(f)
            #CSV has format (DeviceType,DeviceName,Ports)
            for row in reader:
                if(row[0]=="LINK"):
                    continue
                else:
                    node_list.append(Node(row[1],row[0], row[3]))

        for node in node_list:
            print(node)

        # Dynamically assign positions (for visualization)
        x, y = 100, 100  # Starting coordinates
        spacing = 200  # Spacing between nodes
        
        node_positions = {}  # Store positions
        
        # Add nodes from Node_List
        for node in node_list:
            node_positions[node.name] = (x, y)
            self.graph.add_node(node.name, pos=(x, y), type=node.type)
            x += spacing  # Shift position for the next node
            self.graph

        # Adding nodes
        # self.graph.add_node("S1", pos=(100, 100), type="Switch")
        # self.graph.add_node("S2", pos=(300, 100), type="Switch")
        # self.graph.add_node("S3", pos=(500, 100), type="Switch")
        # self.graph.add_node("E1", pos=(100, 250), type="EndStation")
        # self.graph.add_node("E2", pos=(500, 250), type="EndStation")

        # Adding links
        # self.graph.add_edges_from([("S1", "S2"), ("S2", "S3"), ("S1", "E1"), ("S3", "E2"), ("S2", "E2")])
        self.graph.add_edges_from([("sw_0_0","sw_0_3"),("sw_0_3","sw_0_5")])

        # Predefine paths (Streams)
        self.streams = {
            "Stream1": ["E1", "S1", "S2", "S3", "E2"],
            "Stream2": ["E1", "S1", "S3", "E2"]
        }

    def get_stream_path(self, stream_name):
        """ Returns the path for the selected stream """
        return self.streams.get(stream_name, [])


class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node_name, node_type, x, y):
        super().__init__(x - 10, y - 10, 20, 20)  # Circle shape
        self.node_name = node_name
        self.node_type = node_type
        self.setBrush(QBrush(Qt.blue if node_type == "SW" else Qt.green))
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)

        # Create a label for the node
        self.label = QGraphicsTextItem(node_name)
        self.label.setDefaultTextColor(Qt.black)  # Set text color to white
        self.label.setFont(QFont("Arial", 10))  # Set font and size
        self.label.setPos(x-10, y-30)  # Position the label relative to the node

    def mousePressEvent(self, event):
        """ Handles node click event """
        print(f"Clicked on: {self.node_name}")

        #TODO Here we just open a new window, we need a way to pass the switch that has been clicked to this new window
        window2.show()


class UI(QMainWindow):
    def __init__(self, network):
        super().__init__()
        self.setWindowTitle("Interactive Network Topology")
        self.setGeometry(100, 100, 800, 600)
        self.network = network
        self.initUI()

    def initUI(self):
        """ Setup UI layout & elements """
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        main_layout = QVBoxLayout(self.centralWidget)

        # Create the horizontal layout for dropdown and button
        self.layout = QHBoxLayout()
        self.dropdown = QComboBox()
        self.dropdown.addItems(self.network.streams.keys())
        self.dropdown.currentTextChanged.connect(self.highlight_path)
        self.layout.addWidget(self.dropdown)

        self.button = QPushButton("Display Stream")
        self.button.setCheckable(True) #incase we need flags
        self.button.clicked.connect(self.button_was_toggled) #flag method

        self.button.clicked.connect(self.button_clicked) 

        self.layout.addWidget(self.button)

        main_layout.addLayout(self.layout)

        # Create the graphics view for network topology
        self.layout2 = QVBoxLayout()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.layout2.addWidget(self.view)

        main_layout.addLayout(self.layout2)

        # Draw network topology
        self.draw_topology()

    #testing if the button works
    def button_clicked(self):
        print("Button clicked")

    def button_was_toggled(self,checked):
        print("checked", checked)

    def draw_topology(self):
        """ Render the network topology """
        self.node_items = {}
        self.edge_items = {}

        # Draw edges (Links)
        for edge in self.network.graph.edges:
            node1, node2 = edge
            x1, y1 = self.network.graph.nodes[node1]['pos']
            x2, y2 = self.network.graph.nodes[node2]['pos']
            line = self.scene.addLine(x1, y1, x2, y2, QPen(Qt.black, 2))
            self.edge_items[edge] = line

        # Draw nodes (Switches & End Stations)
        for node, data in self.network.graph.nodes(data=True):
            x, y = data["pos"]
            node_item = NodeItem(node, data["type"], x, y)
            node_item.mousePressEvent = node_item.mousePressEvent
            self.scene.addItem(node_item)
            self.scene.addItem(node_item.label)  # Add the label to the scene
            self.node_items[node] = node_item

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

#Just a test to see how we will do deeper views
class secondUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        self.setGeometry(200, 200, 800, 600)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    network = Network()  # Initialize network topology
    window = UI(network)  # Initialize the UI with the network
    window.show()
    window2 = secondUI()
    sys.exit(app.exec_())
    
