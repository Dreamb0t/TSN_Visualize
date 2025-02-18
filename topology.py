import sys
import networkx as nx
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem, QVBoxLayout,QHBoxLayout, QWidget, QComboBox, QPushButton
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt
from enums import *

class NetworkTopology(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interactive Network Topology")
        self.setGeometry(100, 100, 800, 600)

        # Create network graph
        self.graph = nx.Graph()
        self.create_topology()

        # UI Components
        self.initUI()

    def create_topology(self):
        """ Define the network topology (Switches & Endstations) """
        # Adding nodes
        self.graph.add_node("S1", pos=(100, 100), type= type.Switch)
        self.graph.add_node("S2", pos=(300, 100), type= type.Switch)
        self.graph.add_node("S3", pos=(500, 100), type= type.Switch)
        self.graph.add_node("E1", pos=(100, 250), type= type.EndStation)
        self.graph.add_node("E2", pos=(500, 250), type= type.EndStation)

        # Adding links
        self.graph.add_edges_from([("S1", "S2"), ("S2", "S3"), ("S1", "E1"), ("S3", "E2"), ("S2","E2")])

        # Predefine paths (Streams)
        self.streams = {
            "Stream1": ["E1", "S1", "S2", "S3", "E2"],
            "Stream2": ["E1", "S1", "S3", "E2"]
        }

    def initUI(self):
        """ Setup UI layout & elements """
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        main_layout = QVBoxLayout(self.centralWidget)


        layout1 = QHBoxLayout(self.centralWidget) #This contains the dropdown menu and a button for configs
        # Dropdown to select stream
        self.dropdown = QComboBox()
        self.dropdown.addItems(self.streams.keys())
        self.dropdown.currentTextChanged.connect(self.highlight_path)
        layout1.addWidget(self.dropdown)

        #Button
        self.button = QPushButton()
        self.button.clicked.connect(self.image_clicked)
        layout1.addWidget(self.button)

        main_layout.addLayout(layout1)

        layout2 = QVBoxLayout(self.centralWidget)
        # Graphics View for network topology
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout2.addWidget(self.view)

        main_layout.addLayout(layout2)

        # Draw topology
        self.draw_topology()

    def image_clicked(self):
        print("Image clicked")
        print(self)

    def draw_topology(self):
        """ Render the network topology """
        self.node_items = {}
        self.edge_items = {}

        # Draw edges (Links)
        for edge in self.graph.edges:
            node1, node2 = edge
            x1, y1 = self.graph.nodes[node1]['pos']
            x2, y2 = self.graph.nodes[node2]['pos']
            line = self.scene.addLine(x1, y1, x2, y2, QPen(Qt.black, 2))
            self.edge_items[edge] = line

        # Draw nodes (Switches & End Stations)
        for node, data in self.graph.nodes(data=True):
            x, y = data["pos"]
            item = QGraphicsEllipseItem(x-10, y-10, 20, 20)  # Circle shape
            item.setBrush(QBrush(Qt.blue if data["type"] == type.Switch else Qt.green))
            item.setData(0, node)  # Store node name
            item.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
            item.mousePressEvent = self.node_clicked
            self.scene.addItem(item)
            self.node_items[node] = item

    def node_clicked(self, event):
        """ Show node details when clicked """
        clicked_item = event.widget()
        node_name = clicked_item.data(0)
        print(f"Clicked on: {node_name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetworkTopology()
    window.show()
    sys.exit(app.exec_())
