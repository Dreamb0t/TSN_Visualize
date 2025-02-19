import csv
import networkx as nx
from enums import NodeType
from node import *
from streamClass import Stream

graph = nx.DiGraph(name="Links")

def create_graph_from_csv(csv_file):
    """
    Reads a CSV file containing graph link data and constructs a graph.
    
    For each link row (i.e. where the row type equals NodeType.LINK.value),
    the source node adds the target node to its outgoing edges,
    and the target node adds the source node to its ingoing edges.
    
    Expected CSV row format:
      [row_type, name, source, int, target, int, int]
    
    Also, if the target node is a switch, its preceding node is set to the source node.
    
    Returns:
        A dictionary mapping node names to Node objects.
    """
    nodes = {}
    
    with open(csv_file, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            # Process only rows of type LINK.
            if row[0].strip() != NodeType.LINK.value:
                continue

            # Extract fields.
            source_name = row[2].strip()
            target_name = row[4].strip()
            
            # Create or get the source node.
            if source_name not in nodes:
                if source_name.startswith(NodeType.SWITCH.value):
                    nodes[source_name] = Switch(source_name)
                else:
                    nodes[source_name] = EndStation(source_name)
                graph.add_node(nodes[source_name])
            
            # Create or get the target node.
            if target_name not in nodes:
                if target_name.startswith(NodeType.SWITCH.value):
                    nodes[target_name] = Switch(target_name)
                    # Set the preceding node for a switch target.
                    nodes[target_name].set_preceding_node(nodes[source_name])
                else:
                    nodes[target_name] = EndStation(target_name)
                graph.add_node(nodes[target_name])
            else:
                # If the target is already a switch and doesn't have a preceding node, update it.
                node_obj = nodes[target_name]
                if node_obj.type == NodeType.SWITCH and (not node_obj.preceding_node):
                    node_obj.set_preceding_node(nodes[source_name])
            
            # Update the node objects: add out edge for source, in edge for target.
            nodes[source_name].add_out_edge(target_name)
            nodes[target_name].add_in_edge(source_name)
            
            # Add the edge to the NetworkX graph.
            graph.add_edge(source_name, target_name)
    
    return nodes

def _dfs_traverse(node, nodes, target_id, stream, visited, path, prev):
    """
    Helper recursive DFS function.
    
    Args:
        node: The current Node object.
        nodes: Dictionary mapping node names to Node objects.
        target_id: The identifier (string) of the target node.
        stream: The Stream object.
        visited: Set of visited node names.
        path: Current path (list of node names).
        prev: The Node from which we arrived at the current node.
        
    Returns:
        A list of node names representing the path if target is reached; otherwise None.
    """
    # Update the path.
    path = path + [node.name]
    
    # If this node is a switch, record its preceding node.
    if node.type == NodeType.SWITCH and prev is not None:
        node.set_preceding_node(prev)
    
    # If we've reached the target, record the stream size at the destination and return the path.
    if node.name == target_id:
        # For example, store the stream size in an attribute (you may adjust as needed).
        node.stream_size = stream.size
        return path
    
    visited.add(node.name)
    # Get children as union of out_edges and in_edges; sort for determinism.
    children = sorted(set(node.out_edges + node.in_edges))
    for child_name in children:
        if child_name not in visited:
            child_node = nodes.get(child_name)
            if child_node:
                result = _dfs_traverse(child_node, nodes, target_id, stream, visited, path, node)
                if result is not None:
                    return result
    return None

def dfs_traverse_stream(nodes, stream):
    """
    Traverses the graph using DFS based solely on the stream's data.
    
    Args:
        nodes: Dictionary mapping node names to Node objects.
        stream: A Stream object that contains source_node and destination_node.
        
    Returns:
        A list representing the path (list of node names) from stream.source_node to stream.destination_node,
        or None if no path is found.
    """
    start_node = stream.source_node
    if not start_node:
        print(f"Source node {stream.source_node.name} not found.")
        return None
    target_id = stream.destination_node
    return _dfs_traverse(start_node, nodes, target_id, stream, visited=set(), path=[], prev=None)


def bfs_traverse_target(source_node, nodes, target):
    """
    Uses BFS to find the shortest path from source_node to the target node.
    
    Args:
        source_node: The starting Node object.
        nodes: Dictionary mapping node names to Node objects.
        target: The name (string) of the target node.
        
    Returns:
        A list of node names representing the path, or None if no path is found.
    """
    queue = [[source_node.name]]
    visited = set()
    
    while queue:
        path = queue.pop(0)
        last_node_name = path[-1]
        if last_node_name == target:
            return path
        if last_node_name not in visited:
            visited.add(last_node_name)
            current_node = nodes.get(last_node_name)
            if current_node:
                children = sorted(set(current_node.out_edges + current_node.in_edges))
                for child in children:
                    if child not in path:
                        new_path = path + [child]
                        queue.append(new_path)
    return None

def allStreams(csv_file):
    """
    Processes a streams CSV file with the following structure:
      PCP, StreamName, StreamType, SourceNode, DestinationNode, Size, Period, Deadline
    For each stream, it finds a path (using DFS) from the source node to the destination node.
    """
    with open(csv_file, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            # Unpack the stream details.
            pcp = row[0].strip()
            stream_id = row[1].strip()
            stream_type = row[2].strip()
            source_node = nodes[row[3].strip()]
            target_node = nodes[row[4].strip()]
            size = row[5].strip()
            period = row[6].strip()
            deadline = row[7].strip()

            s = Stream(pcp, stream_id, stream_type, source_node, target_node, size, period, deadline)
            # Get the source and target Node objects.

            if not source_node or not target_node:
                print(f"Stream {stream_id}: Source or target node not found.")
                continue
            
            path = dfs_traverse_stream(nodes, s)
            if path:
                print("Stream:", s.stream_name)
                print("---DFS PATH---")
                print("Nodes traversed:", len(path))
                print(" -> ".join(path))        
                # Optionally, print target node's stored stream size:
                target_node = nodes.get(s.destination_node)
                if target_node and hasattr(target_node, 'stream_size'):
                    print(f"Target {target_node.name} stored stream size: {target_node.stream_size}")
                else:
                    print(f"Stream {s.stream_name}: No path found from {s.source_node} to {s.destination_node}.")

# Main execution
if __name__ == "__main__":
    csv_file_path = "topology.csv"  # CSV with LINK rows
    nodes = create_graph_from_csv(csv_file_path)
    
    # Uncomment the following if you wish to draw the graph with NetworkX:
    # nx.draw(graph, with_labels=True)
    
    print("DFS traversal starting")
    allStreams("streams.csv")
