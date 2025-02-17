import csv

#TODO look into adding necessarry attributes to nodes, to make DOT formating (for graphviz) easier
class Node:
    def __init__(self,name,type):
        self.name = name
        self.type = type

    #To give a quick summation of what the object contains also
    def __str__(self):
        return f"{self.name} is a {self.type}"

class PPNode(Node):
    # We give the child Node the class attribute "format" to distinguish between formats. This should be the same
    #for all nodes that come from a PP file.
    format = "PPNode"
    def __init__(self, name, type,ports):
        super().__init__(name, type)
        self.ports = ports

    #includes the format
    def __str__(self):
        return super().__str__() + ", format is of " + f"{self.format}"

Node_List = []

#TODO make a guide, that tells the user, the csv file should be called something specific 
#(maybe also have a dedicated path) in the folder
with open("topology.csv", "r") as f:
    reader = csv.reader(f)
    #CSV has format (DeviceType,DeviceName,Ports)
    for row in reader:
        # if(row[0]=="SW"):
        Node_List.append(Node(row[1],row[0], row[3]))

for node in Node_List:
    print(node)

