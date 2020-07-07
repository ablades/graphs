from graphs.graph import Graph, Vertex


class WeightedVertex(Vertex):

    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors dictionary.
        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.__id = vertex_id
        self.__neighbors_dict = {}  # id -> (obj, weight)

    def add_neighbor(self, vertex_obj, weight):
        """
        Add a neighbor by storing it in the neighbors dictionary.
        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        weight (number): The weight of this edge.
        """
        if vertex_obj.get_id() in self.__neighbors_dict.keys():
            return  # it's already a neighbor

        self.__neighbors_dict[vertex_obj.get_id()] = (vertex_obj, weight)

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        return [neighbor for (neighbor, weight) in self.__neighbors_dict.values()]

    def get_neighbors_with_weights(self):
        """Return the neighbors of this vertex."""
        return list(self.__neighbors_dict.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.__id

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = [neighbor.get_id() for neighbor in self.get_neighbors()]
        return f'{self.__id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = [neighbor.get_id() for neighbor in self.get_neighbors()]
        return f'{self.__id} adjacent to {neighbor_ids}'


class WeightedGraph(Graph):

    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.
        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.__vertex_dict = {}
        self.__is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.
        Parameters:
        vertex_id (string): The unique identifier for the new vertex.
        Returns:
        Vertex: The new vertex object.
        """
        if vertex_id in self.__vertex_dict.keys():
            return False  # it's already there
        vertex_obj = WeightedVertex(vertex_id)
        self.__vertex_dict[vertex_id] = vertex_obj
        return True

    def get_vertex(self, vertex_id):
        """Return the vertex if it exists."""
        if vertex_id not in self.__vertex_dict.keys():
            return None
        vertex_obj = self.__vertex_dict[vertex_id]
        return vertex_obj

    def add_edge(self, vertex_id1, vertex_id2, weight):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.
        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        weight (number): The edge weight.
        """
        all_ids = self.__vertex_dict.keys()
        if vertex_id1 not in all_ids or vertex_id2 not in all_ids:
            return False
        vertex_obj1 = self.get_vertex(vertex_id1)
        vertex_obj2 = self.get_vertex(vertex_id2)
        vertex_obj1.add_neighbor(vertex_obj2, weight)
        if not self.__is_directed:
            vertex_obj2.add_neighbor(vertex_obj1, weight)

    def get_vertices(self):
        """Return all the vertices in the graph"""
        return list(self.__vertex_dict.values())

    def get_edges(self):
        """Return all the edges in the graph"""
        return list()

    def __iter__(self):
        """Iterate over the vertex objects in the graph, to use sytax:
        for vertex in graph"""
        return iter(self.__vertex_dict.values())

    def union(self, parent_map, vertex_id1, vertex_id2):
        """Combine vertex_id1 and vertex_id2 into the same group."""
        vertex1_root = self.find(parent_map, vertex_id1)
        vertex2_root = self.find(parent_map, vertex_id2)
        parent_map[vertex1_root] = vertex2_root

    def find(self, parent_map, vertex_id):
        """Get the root (or, group label) for vertex_id."""
        if parent_map[vertex_id] == vertex_id:
            return vertex_id
        return self.find(parent_map, parent_map[vertex_id])

    def minimum_spanning_tree_kruskal(self):
        """
        Use Kruskal's Algorithm to return a list of edges, as tuples of 
        (start_id, dest_id, weight) in the graph's minimum spanning tree.
        """
        #
        edges = list()

        # Create and sort edges
        for _, vertex in enumerate(self.get_vertices()):
            for _, (neighbor, weight) in enumerate(vertex.get_neighbors_with_weights()):
                edges.append((vertex.get_id(), neighbor.get_id(), weight))

        edges = sorted(edges, key=lambda x: x[2])

        parent_map = dict()
        for _, vertex in enumerate(edges):
            parent_map[vertex[0]] = vertex[0]

        # Solution tree
        spanning_tree = list()

        while len(spanning_tree) <= len(edges) - 1:
            # Process an edge
            edge = edges.pop(0)
            vertex1, vertex2, weight = edge
            # Determine if vertexes should be joined
            if self.find(parent_map, vertex1) != self.find(parent_map, vertex2):
                spanning_tree.append(edge)
                self.union(parent_map, vertex1, vertex2)

        return spanning_tree

    def minimum_spanning_tree_prim(self):
        """
        Use Prim's Algorithm to return the total weight of all edges in the
        graph's spanning tree.
        Assume that the graph is connected.
        """
        total_weight = 0
        vertex_weights = dict()
        # Add all verticies
        for _, vertex in enumerate(self.get_vertices()):
            vertex_weights[vertex] = float('inf')

        vertex_weights[self.get_vertices()[0]] = 0

        while vertex_weights:
            # Find min, increment weight
            min_vertex = min(vertex_weights.items(), key=lambda v: v[1])
            vertex = min_vertex[0]
            vertex_weights.pop(vertex, None)
            total_weight += min_vertex[1]

            for _, (neighbor, weight) in enumerate(vertex.get_neighbors_with_weights()):
                # Assign weight
                if neighbor in vertex_weights and weight < vertex_weights[neighbor]:
                    vertex_weights[neighbor] = weight

        return total_weight

    def find_shortest_path(self, start_id, target_id):
        """
        Use Dijkstra's Algorithm to return the total weight of the shortest path
        from a start vertex to a destination.
        """
        vertex_distances = dict()
        # Add all verticies
        for _, vertex in enumerate(self.get_vertices()):
            vertex_distances[vertex] = float('inf')

        # Set starting vertex distance
        vertex_distances[self.get_vertex(start_id)] = 0

        while vertex_distances:
            # Find min vertex
            min_vertex = min(vertex_distances.items(), key=lambda d: d[1])

            # Remove it from the dictionary. 
            vertex_distances.pop(min_vertex[0])

            # Found target, return
            if min_vertex[0].get_id() == target_id:
                return min_vertex[1]
            else:
                # Update weight of still existing neighboors
                for _, (vertex, weight) in enumerate(min_vertex[0].get_neighbors_with_weights()):
                    if vertex in vertex_distances and weight + min_vertex[1] < vertex_distances[vertex]:
                        vertex_distances[vertex] = weight + min_vertex[1]

        return None

    def floyd_warshall(self):
        """
        Return the All-Pairs-Shortest-Paths dictionary, containing the shortest
        paths from each vertex to each other vertex.
        """
        # create a top-level dictionary to hold each vertex & map it to another
        # dictionary
        dist = dict()
        all_vertex_ids = self.__vertex_dict.keys()
        # set default values - either 0 (for v -> v) or infinity
        for vertex1 in all_vertex_ids:
            dist[vertex1] = dict()
            for vertex2 in all_vertex_ids:
                dist[vertex1][vertex2] = float('inf')
            dist[vertex1][vertex1] = 0
        # add all edge weights to the dictionary
        all_vertex_objs = self.get_vertices()
        for vertex in all_vertex_objs:
            neighbors_with_weights = vertex.get_neighbors_with_weights()
            for neighbor, weight in neighbors_with_weights:
                dist[vertex.get_id()][neighbor.get_id()] = weight
        # execute the algorithm - "relax" the distances using an intermediate vertex
        for k in all_vertex_ids:
            for i in all_vertex_ids:
                for j in all_vertex_ids:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        return dist
