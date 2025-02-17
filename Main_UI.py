import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QIcon, QPixmap

class TopologyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TSN Topology")
        # self.setGeometry() #To set placement and dimensions(x,y,width,height)
        self.setWindowIcon(QIcon("Icon.png"))

        self.initUI()


    def initUI(self):
        central_widget = QWidget(self)  # Create a central widget
        layout = QVBoxLayout(central_widget)  # Assign layout to the central widget

        # Create a QPushButton
        button = QPushButton()

        image_path = "images/switch.jpg"
        if not os.path.exists(image_path):
            print(f"Error: Image not found at {image_path}")
        else:
            # Load the image
            pixmap = QPixmap(image_path)
            button.setIcon(QIcon(pixmap))
            button.setIconSize(pixmap.size())
            button.setFixedSize(pixmap.size())  # Set exact size of the button

            # button.setFlat(True)  #remove button border not necessary since we dont see it anyway anymore.
            
            # Connect the button's clicked signal
            button.clicked.connect(self.image_clicked)

        layout.addWidget(button)

        self.setCentralWidget(central_widget)  # Set the central widget


    def image_clicked(self):
        print("Image button clicked!")

def main():
    app = QApplication(sys.argv)
    window = TopologyWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()