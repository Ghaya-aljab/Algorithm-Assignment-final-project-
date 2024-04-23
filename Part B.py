import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.graph = {}
        self.vertices_info = {}

    def add_vertex(self, vertex, vertex_id):
        if vertex not in self.graph:
            self.graph[vertex] = []
            self.vertices_info[vertex] = {'id': vertex_id}

    def add_edge(self, source, destination, road_id, road_name, length, congestion_level=0):
        if source not in self.graph:
            self.add_vertex(source, source)
        if destination not in self.graph:
            self.add_vertex(destination, destination)

        edge = {'id': road_id, 'name': road_name, 'length': length, 'congestion_level': congestion_level,
                'original_length': length}
        self.graph[source].append((destination, edge))
        self.graph[destination].append((source, edge))

    def add_house(self, house_id, intersection, distance):
        if intersection not in self.graph:
            self.add_vertex(intersection, intersection)
        edge = {'name': 'virtual', 'length': distance, 'original_length': distance, 'congestion_level': 0}
        self.graph[house_id] = [(intersection, edge)]
        self.graph[intersection].append((house_id, edge))

    def get_neighbors(self, vertex):
        return self.graph.get(vertex, [])

def dijkstra(graph, source):
    distances = {vertex: float('inf') for vertex in graph.graph}
    distances[source] = 0
    priority_queue = [(0, source)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        if current_distance > distances[current_vertex]:
            continue
        for neighbor, edge in graph.get_neighbors(current_vertex):
            distance = current_distance + edge['length']
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

def optimize_traffic_flow(graph):
    for vertex in graph.graph:
        for neighbor, edge in graph.get_neighbors(vertex):
            if 'original_length' in edge:  # Ensure all edges have 'original_length' before processing
                edge['length'] = calculate_updated_weight(edge['original_length'], edge['congestion_level'])
    return graph

def calculate_updated_weight(length, congestion_level):
    return length * (1 + congestion_level)

def distribute_packages(graph, source):
    distances = dijkstra(graph, source)
    return distances

def find_shortest_distance(graph, source, target):
    distances = dijkstra(graph, source)
    shortest_distance = distances[target]
    return shortest_distance

def create_road_network():
    graph = Graph()

    intersections = [('A', 'A1'), ('B', 'B1'), ('C', 'C1'), ('D', 'D1'), ('E', 'E1'), ('F', 'F1')]
    for intersection, id in intersections:
        graph.add_vertex(intersection, id)

    graph.add_edge('A', 'B', 'R1', 'Road 1', 5)
    graph.add_edge('A', 'C', 'R2', 'Road 2', 3)
    graph.add_edge('B', 'C', 'R3', 'Road 3', 2)
    graph.add_edge('B', 'D', 'R4', 'Road 4', 4)
    graph.add_edge('C', 'E', 'R5', 'Road 5', 6)
    graph.add_edge('D', 'E', 'R6', 'Road 6', 1)
    graph.add_edge('D', 'F', 'R7', 'Road 7', 2)
    graph.add_edge('E', 'F', 'R8', 'Road 8', 3)

    graph.add_house('H1', 'B', 1)
    graph.add_house('H2', 'E', 3)
    graph.add_house('H3', 'D', 2)
    graph.add_house('H4', 'C', 4)

    return graph

road_network = create_road_network()
optimized_network = optimize_traffic_flow(road_network)

def display_menu():
    print("---" * 10, "MENU", "---" * 10)
    print("1. Distribute packages from a source intersection")
    print("2. View the road network")
    print("3. View the list of homes")
    print("4. Exit")

def create_networkx_graph(graph):
    G = nx.Graph()
    for vertex, edges in graph.graph.items():
        for neighbor, edge in edges:
            G.add_edge(vertex, neighbor, **edge)
    return G

def visualize_graph(graph, shortest_path=None, source=None, destination=None):
    G = nx.Graph()
    houses = []
    for vertex, edges in graph.graph.items():
        for neighbor, edge in edges:
            G.add_edge(vertex, neighbor, **edge)
        if vertex.startswith('H'):  # If the vertex represents a house
            houses.append(vertex)

    pos = nx.spring_layout(G)  # Positions for all nodes

    plt.figure(figsize=(10, 8))

    # Draw edges
    nx.draw_networkx_edges(G, pos, width=2)

    # Draw nodes for intersections
    nx.draw_networkx_nodes(G, pos, nodelist=[node for node in G if node not in houses],
                           node_color='skyblue', node_size=700)

    # Draw nodes for houses
    nx.draw_networkx_nodes(G, pos, nodelist=houses, node_color='orange', node_size=700)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif")

    # Draw edge labels
    edge_labels = {(u, v): f"{d['name']}\n({d['length']} km)" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Highlight shortest path
    if shortest_path:
        path_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color='lightgreen')

    # Highlight source intersection
    if source:
        nx.draw_networkx_nodes(G, pos, nodelist=[source], node_color='yellow', node_size=700)

    # Highlight destination house
    if destination:
        nx.draw_networkx_nodes(G, pos, nodelist=[destination], node_color='red', node_size=700)

    plt.title("Road Network Graph")
    plt.axis('off')  # Turn off axis
    plt.show()

def main():
    road_network = create_road_network()

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            print("---" * 10, "PACKAGE DISTRIBUTION", "---" * 10)
            print("Intersections: ")
            for intersection in road_network.graph:
                if not intersection.startswith('H'):
                    print(intersection)
            print("")
            source_intersection = input("Enter the source intersection: ")
            if source_intersection not in road_network.graph:
                print("Invalid intersection.")
                continue
            print("--" * 33)
            print("Houses:")
            for house, edges in road_network.graph.items():
                if house.startswith('H'):
                    print(house)
            destination_house = input("Enter the destination house: ")
            if destination_house not in road_network.graph:
                print("Invalid house.")
                continue
            print("")
            package_distance = find_shortest_distance(optimized_network, source_intersection, destination_house)
            print(f"The shortest distance from {source_intersection} to {destination_house} is {package_distance}")
            networkx_graph = create_networkx_graph(optimized_network)
            shortest_path = nx.shortest_path(networkx_graph, source_intersection, destination_house)
            visualize_graph(road_network, shortest_path, source=source_intersection, destination=destination_house)


        elif choice == '2':
            visualize_graph(road_network)
        elif choice == '3':
            print("")
            print("---" * 10, "HOMES", "---" * 10)
            for house, edges in road_network.graph.items():
                if house.startswith('H'):
                    print(f"House ID: {house}")
                    for edge in edges:
                        print(f"- Intersection: {edge[0]}, Distance: {edge[1]['length']}")
            print("")
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
