from PyQt5.QtGui import QPen, QBrush, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QPushButton
from PyQt5.QtGui import QPen, QBrush, QFont
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import networkx as nx
from enums.deviceEnums import NodeType
from .nodeClass import Node

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node: Node, x, y):
        super().__init__(x - 10, y - 10, 20, 20)  # Circle shape
        self.node = node  # Store the Node instance
        self.setBrush(QBrush(Qt.blue if node.type == NodeType.SWITCH else Qt.green))
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)

        # Create a label for the node
        self.label = QGraphicsTextItem(node.name)
        self.label.setDefaultTextColor(Qt.black)
        self.label.setFont(QFont("Arial", 10))
        self.label.setPos(x-10, y-30)

    def mousePressEvent(self, event):
        print(f"Clicked on: {self.node.name}, Type: {self.node.type.value}, Port: {self.node.port}")
        self.window2 = SecondUI(self.node)  # Store a reference on 'self'
        self.window2.show()


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
        """Render the network topology using node objects as keys."""
        self.node_items = {}
        self.edge_items = {}
        
        # Compute positions using spring_layout. Keys are Node objects.
        pos = nx.spring_layout(self.network.graph, seed=42, scale=200)
        for node_obj, (x, y) in pos.items():
            # Store the computed position in the graph data.
            self.network.graph.nodes[node_obj]["pos"] = (x + 50, y + 50)
        
        # Draw edges.
        for edge in self.network.graph.edges:
            node1, node2 = edge  # Both are Node objects.
            x1, y1 = self.network.graph.nodes[node1]["pos"]
            x2, y2 = self.network.graph.nodes[node2]["pos"]
            line = self.scene.addLine(x1, y1, x2, y2, QPen(Qt.black, 2))
            self.edge_items[edge] = line

        # Draw nodes.
        for node_obj, data in self.network.graph.nodes(data=True):
            if "node_obj" not in data:
                print(f"Warning: Missing node data for {node_obj}")
                continue
            # Retrieve the node object and its position.
            node = data["node_obj"]
            x, y = data["pos"]
            node_item = NodeItem(node, x, y)
            self.scene.addItem(node_item)
            self.scene.addItem(node_item.label)
            self.node_items[node.name] = node_item



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
    def __init__(self, node):
        super().__init__()
        self.node = node
        self.setWindowTitle(node.name)
        self.setGeometry(200, 200, 800, 600)
        self.initUI()

    def initUI(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)
        
        # Create a read-only text edit to display traffic
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        layout.addWidget(self.textEdit)
        
        # Format and set the traffic information in the text edit
        if self.node.type == NodeType.SWITCH:
            self.textEdit.setText(self.formatTraffic())
        else:
            self.textEdit.setText(self.formatArrivalTimes())

    def formatArrivalTimes(self):
        if not self.node.arrivals:
            return "No arrivals recorded."
        formatted_arrivals = []
        for rec in self.node.arrivals:
            # Use .get() to provide defaults if keys are missing
            source = rec.get("source node name", "Unknown")
            data_size = rec.get("data size", "N/A")
            arrival_time = rec.get("arrival_time", "N/A")
            formatted_arrivals.append(f"{source} -> {data_size} at {arrival_time}")
        return "\n".join(formatted_arrivals)

    
    def formatTraffic(self):
        # Check if traffic data exists.
        if not self.node.traffic:
            return "No traffic available."

        # Build a formatted string from the node's traffic dictionary.
        lines = []
        for stream_id, info in self.node.traffic.items():
            # Get the previous node's name if available.
            previous_node = info.get('previous_node')
            previous_node_name = previous_node.name if previous_node else "None"
            data_size = info.get('data_size', "N/A")
            time = info.get('time', "N/A")
            line = f"Stream: {stream_id} | From: {previous_node_name} | Data Size: {data_size} | Time: {time}"
            lines.append(line)
        return "\n".join(lines)