import sys
from Classes.networkClass import Network
from Classes.UI_Classes import *

topologyCSV = "./csv-files/topology.csv"
streamsCSV = "./csv-files/streams.csv"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    network = Network(topologyCSV, streamsCSV)
    window = UI(network)
    window.show()
    sys.exit(app.exec_())
