class Stream:
    def __init__(self, name, source_node, destination_node):
        self.name = name
        self.source = source_node
        self.destination = destination_node
        self.path = []