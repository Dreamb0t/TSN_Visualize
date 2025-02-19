
class Node:
    def __init__(self, name, type, port):
        self.name = name
        self.type = type
        self.port = port

    def __str__(self):
        return f"{self.name} ({self.type}, Port: {self.port})"