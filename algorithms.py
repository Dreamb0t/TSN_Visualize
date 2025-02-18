import csv
import networkx as nx
from node import Node  # Your Node class with in_edges and out_edges lists
from enums import NodeType

graph = nx.DiGraph(name = "Links")

def create_graph_from_csv(csv_file):
    """
    Reads a CSV file containing graph link data and constructs a graph.
    
    For each link row (i.e. where the row type equals NodeType.LINK.value),
    the source node adds the target node to its outgoing edges,
    and the target node adds the source node to its ingoing edges.
    
    Expected CSV row format:
      [row_type, name, source, int, target, int, int]
    
    Returns:
        A tuple (nodes, graph)
          - nodes: a dictionary mapping node names to Node objects.
          - graph: a NetworkX DiGraph constructed from the links.
    """
    nodes = {}
    
    
    with open(csv_file, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            # Process only rows that are of type LINK.
            if row[0].strip() != NodeType.LINK.value:
                continue

            # Extract fields from CSV.
            source_name = row[2].strip()
            target_name = row[4].strip()
            
            # Create or get the source node.
            if source_name not in nodes:
                # Decide type based on naming convention (or other CSV data)
                if source_name.startswith(NodeType.SWITCH.value):
                    source_type = NodeType.SWITCH
                else:
                    source_type = NodeType.ENDSTATION
                nodes[source_name] = Node(source_name, source_type)
                graph.add_node(source_name, type=source_type.value)
            # Create or get the target node.
            if target_name not in nodes:
                if target_name.startswith(NodeType.SWITCH.value):
                    target_type = NodeType.SWITCH
                else:
                    target_type = NodeType.ENDSTATION
                nodes[target_name] = Node(target_name, target_type)
                graph.add_node(target_name, type=target_type.value)
            
            # Update the Node objects.
            nodes[source_name].add_out_edge(target_name)
            nodes[target_name].add_in_edge(source_name)
            
            # Add the edge to the NetworkX graph.
            graph.add_edge(source_name, target_name)
    
    return nodes

def dfs_traverse_target(node, nodes, target, visited=None, path=None):
    """
    Recursively traverses the graph using DFS until the target node is reached.
    
    Args:
        node: The current Node object to visit.
        nodes: A dictionary mapping node names to Node objects.
        target: The name of the target node to reach.
        visited: A set of node names that have been visited.
        path: The current path as a list of node names.
    
    Returns:
        A list representing the path from the starting node to the target node,
        or None if no such path exists.
    """
    if visited is None:
        visited = set()
    if path is None:
        path = []
    
    # Add the current node to the path.
    path = path + [node.name]
    
    # If we've reached the target, return the path.
    if node.name == target.name:
        #print("---------FOUND---------")
        return path
    
    # Mark this node as visited.
    visited.add(node.name)
    #print(node.name)
    # Define children as the union of outgoing and ingoing edges.
    children = sorted(set(node.out_edges + node.in_edges))
    
    # Recursively search for the target in each child.
    for child_name in children:
        if child_name not in visited:
            child_node = nodes.get(child_name)
            if child_node:
                result = dfs_traverse_target(child_node, nodes, target, visited, path)
                if result is not None:
                    return result
    return None

def bfs_traverse_target(source_node, nodes, target):
    """
    Traverses the graph using BFS to find the shortest path from source_node to target.
    
    Args:
        source_node: The starting Node object.
        nodes: A dictionary mapping node names to Node objects.
        target: The name of the target node.
        
    Returns:
        A list of node names representing the path from the source to the target,
        or None if no path exists.
    """
    # Initialize a queue with the starting path.
    queue = [[source_node.name]]
    
    # A set to keep track of visited nodes.
    visited = set()
    
    while queue:
        # Pop the first path from the queue.
        path = queue.pop(0)
        last_node_name = path[-1]
        
        # If we've reached the target, return the path.
        if last_node_name == target:
            return path
        
        # Mark the current node as visited.
        if last_node_name not in visited:
            visited.add(last_node_name)
            
            # Get the current node.
            current_node = nodes.get(last_node_name)
            if current_node:
                # Get all children (neighbors) as the union of in_edges and out_edges.
                children = sorted(set(current_node.out_edges + current_node.in_edges))
                for child in children:
                    # Avoid cycles: only add child if it's not already in the current path.
                    if child not in path:
                        new_path = path + [child]
                        queue.append(new_path)
                        
    # No path found.
    return None

def allStreams(csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            stream_id = row[1]
            # Extract fields from CSV.

            source = row[3].strip()
            target = row[4].strip()

                # Example: prompt the user for source and target nodes.
            source_node = nodes[source]#input("Enter the source node: ").strip()
            target_node = nodes[target]#input("Enter the target node: ").strip()
            path = dfs_traverse_target(source_node, nodes, target_node)
            #path2 = bfs_traverse_target(source_node, nodes, target_node)
            if(path):
                print("Path found for:")
                print(stream_id)
                print("---DFS PATH---")
                print(len(path))
                print(path)
            


if __name__ == "__main__":
    csv_file_path = "topology.csv"  # Replace with your CSV file path
    nodes = create_graph_from_csv(csv_file_path)
    


    #nx.draw(graph)

    print("DFS traversal starting")
    allStreams("streams.csv")
    #print("------- BFS PATH---------")
    #print(len(path2))
    #print(path2)
    
