from graphs.graph import Graph, Vertex


class WeightedVertex(Vertex):
    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors.

        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.__id = vertex_id
        self.__neighbors_dict = {} # id -> (obj, weight)

    def add_neighbor(self, vertex_obj, weight):
        """
        Add a neighbor along a weighted edge by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        weight (int): The edge weight from self -> neighbor.
        """
        self.__neighbors_dict[vertex_obj._id] = (vertex_obj, weight)

    def get_neighbors(self):
        """Return the neighbors of this vertex as a list of neighbor ids."""
        neighbors_list = list()

        for key, _ in enumerate(self.__neighbors_dict):
            neighbors_list.append(key)

        return neighbors_list

    def get_neighbors_with_weights(self):
        """Return the neighbors of this vertex as a list of tuples of (neighbor_id, weight)."""
        neighbors_list = list()

        for key, value in enumerate(self.__neighbors_dict):
            neighbors_list.append((key, value[1]))

        return neighbors_list


class WeightedGraph(Graph):
    def __init__(self, is_directed=True):
        """
        Initialize a weighted graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.vertex_dict = {} # id -> object
        self.__is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.

        Parameters:
        vertex_id (string): The unique identifier for the new vertex.

        Returns:
        Vertex: The new vertex object.
        """
        # TODO: Implement this function.
        pass

    def add_edge(self, vertex_id1, vertex_id2, weight):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        """
        # TODO: Implement this function.
        pass
