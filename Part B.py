import heapq


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

    def add_house(self, house_id, intersection, road_id, distance):
        if intersection not in self.graph:
            self.add_vertex(intersection, intersection)
        edge = {'id': road_id, 'name': 'virtual', 'length': distance, 'original_length': distance,
                'congestion_level': 0}
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

    graph.add_house('H1', 'B', 'R7', 1)
    graph.add_house('H2', 'E','R4', 3)

    return graph


road_network = create_road_network()

optimized_network = optimize_traffic_flow(road_network)

source_intersection = 'A'
package_distances = distribute_packages(optimized_network, source_intersection)
print("Package distribution distances:")
for intersection, distance in package_distances.items():
    print(f"Intersection: {intersection}, Distance: {distance}")

source_intersection = 'A'
target_intersection = 'F'
shortest_distance = find_shortest_distance(optimized_network, source_intersection, target_intersection)
print(f"The shortest distance from {source_intersection} to {target_intersection} is {shortest_distance}")
