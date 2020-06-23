from collections import deque


class Vertex(object):
    """
    Defines a single vertex and its neighbors.
    """

    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors dictionary.

        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.__id = vertex_id
        self.__neighbors_dict = {}  # id -> object

    def add_neighbor(self, vertex_obj):
        """
        Add a neighbor by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        """
        self.__neighbors_dict[vertex_obj.get_id()] = vertex_obj

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = list(self.__neighbors_dict.keys())
        return f'{self.__id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        return self.__str__()

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        return list(self.__neighbors_dict.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.__id


class Graph:
    """ Graph Class
    Represents a directed or undirected graph.
    """
    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.__vertex_dict = {}  # id -> object
        self.__is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.

        Parameters:
        vertex_id (string): The unique identifier for the new vertex.

        Returns:
        Vertex: The new vertex object.
        """

        self.__vertex_dict[vertex_id] = Vertex(vertex_id)

        return self.__vertex_dict.get(vertex_id)

    def get_vertex(self, vertex_id):
        """Return the vertex if it exists."""
        if vertex_id not in self.__vertex_dict:
            return None

        vertex_obj = self.__vertex_dict[vertex_id]
        return vertex_obj

    def add_edge(self, vertex_id1, vertex_id2):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        """
        if self.get_vertex(vertex_id1) is None:
            self.add_vertex(vertex_id1)

        if self.get_vertex(vertex_id2) is None:
            self.add_vertex(vertex_id2)

        self.__vertex_dict[vertex_id1].add_neighbor(self.__vertex_dict[vertex_id2])

        if not self.__is_directed:
            self.__vertex_dict[vertex_id2].add_neighbor(self.__vertex_dict[vertex_id1])

    def get_vertices(self):
        """
        Return all vertices in the graph.

        Returns:
        List<Vertex>: The vertex objects contained in the graph.
        """
        return list(self.__vertex_dict.values())

    def contains_id(self, vertex_id):
        return vertex_id in self.__vertex_dict

    def __str__(self):
        """Return a string representation of the graph."""
        return f'Graph with vertices: {self.get_vertices()}'

    def __repr__(self):
        """Return a string representation of the graph."""
        return self.__str__()

    def bfs_traversal(self, start_id):
        """
        Traverse the graph using breadth-first search.
        """
        if not self.contains_id(start_id):
            raise KeyError("One or both vertices are not in the graph!")

        # Keep a set to denote which vertices we've seen before
        seen = set()
        seen.add(start_id)

        # Keep a queue so that we visit vertices in the appropriate order
        queue = deque()
        queue.append(self.get_vertex(start_id))

        while queue:
            current_vertex_obj = queue.popleft()
            current_vertex_id = current_vertex_obj.get_id()

            # Process current node
            print('Processing vertex {}'.format(current_vertex_id))

            # Add its neighbors to the queue
            for neighbor in current_vertex_obj.get_neighbors():
                if neighbor.get_id() not in seen:
                    seen.add(neighbor.get_id())
                    queue.append(neighbor)

        return  # everything has been processed

    def find_shortest_path(self, start_id, target_id):
        """
        Find and return the shortest path from start_id to target_id.

        Parameters:
        start_id (string): The id of the start vertex.
        target_id (string): The id of the target (end) vertex.

        Returns:
        list<string>: A list of all vertex ids in the shortest path, from start to end.
        """
        if not self.contains_id(start_id) or not self.contains_id(target_id):
            raise KeyError("One or both vertices are not in the graph!")

        # vertex keys we've seen before and their paths from the start vertex
        vertex_id_to_path = {
            start_id: [start_id]  # only one thing in the path
        }

        # queue of vertices to visit next
        queue = deque()
        queue.append(self.get_vertex(start_id))

        # while queue is not empty
        while queue:
            current_vertex_obj = queue.popleft()   # vertex obj to visit next
            current_vertex_id = current_vertex_obj.get_id()

            # found target, can stop the loop early
            if current_vertex_id == target_id:
                break

            neighbors = current_vertex_obj.get_neighbors()
            for neighbor in neighbors:
                if neighbor.get_id() not in vertex_id_to_path:
                    current_path = vertex_id_to_path[current_vertex_id]
                    # extend the path by 1 vertex
                    next_path = current_path + [neighbor.get_id()]
                    vertex_id_to_path[neighbor.get_id()] = next_path
                    queue.append(neighbor)
                    # print(vertex_id_to_path)

        if target_id not in vertex_id_to_path:   # path not found
            return None

        return vertex_id_to_path[target_id]

    def find_vertices_n_away(self, start_id, target_distance):
        """
        Find and return all vertices n distance away.

        Arguments:
        start_id (string): The id of the start vertex.
        target_distance (integer): The distance from the start vertex we are looking for

        Returns:
        list<string>: All vertex ids that are `target_distance` away from the start vertex
        """
        # vertices that have already been seen
        visited = set()
        # holds verticies and shortest paths
        target_vertices = []

        # build queue add first item
        queue = deque()
        # add tuple to queue with id and distance
        queue.append((start_id, 0))
        visited.add(start_id)

        # perform bfs
        while queue:
            # take item off queue
            v = queue.popleft()

            # add item if it matches distance
            if v[1] == target_distance:
                target_vertices.append(v[0])

            # add adjacent verticies
            for _, vertex in enumerate(self.get_vertex(v[0]).get_neighbors()):
                # add vertex to queue mark as seen
                if vertex.get_id() not in visited:
                    queue.append((vertex.get_id(), v[1] + 1))
                    visited.add(vertex.get_id())

        return target_vertices

    def is_bipartite(self):
        """
        Return True if the graph is bipartite, and False otherwise.
        """
        start_id = self.get_vertices()[0].get_id()
        visited = {}
        # build queue add first item
        queue = deque()
        next_color = "r"
        queue.append(start_id)
        visited[start_id] = next_color

        while queue:
            # swap color
            if next_color == "r":
                next_color = "b"
            else:
                next_color = "r"

            current_vertex = self.get_vertex(queue.popleft())

            # loop over adjcent vertexes
            for _, vertex in enumerate(current_vertex.get_neighbors()):
                vertex_color = visited.get(vertex.get_id(), None)
                current_color = visited.get(current_vertex.get_id(), None)

                # graph is not bipartite if vertex is same color as current node
                if vertex_color == current_color:
                    return False
                # vertex has not been seen give it a color, add it to queue
                elif vertex_color is None:
                    visited[vertex.get_id()] = next_color
                    queue.append(vertex.get_id())

        return True

    def get_connected(self, start_id, visit):
        """
        Helper function that performs bfs and returns a list of connected components
        """
        visited = set()
        # build queue add first item
        queue = deque()
        queue.append(start_id)
        visited.add(start_id)

        while queue:
            v = self.get_vertex(queue.popleft())

            # add adj verticies
            for _, vertex in enumerate(v.get_neighbors()):
                # add vertex to queue mark as visited and pass to visit function
                if vertex.get_id() not in visited:
                    queue.append((vertex.get_id()))
                    visited.add(vertex.get_id())
                    visit(vertex.get_id())

        return list(visited)

    def find_connected_components(self):
        """
        Return a list of all connected components, with each connected component
        represented as a list of vertex ids.
        """

        vertices = self.get_vertices()
        visited = set()
        cc = list()

        # loop over each vertex
        for _, vertex in enumerate(vertices):
            # vertex has not been visited perform bfs
            if vertex.get_id() not in visited:
                visited.add(vertex.get_id())
                cc.append(self.get_connected(vertex.get_id(), visited.add))

        return cc

    def find_path_dfs_iter(self, start_id, target_id):
        """
        Use DFS with a stack to find a path from start_id to target_id.
        """

        visited = set()
        stack = deque()
        stack.append(start_id)
        visited.add(start_id)

        path = list()

        while stack:
            v = self.get_vertex(stack.pop())
            path.append(v.get_id())

            if v.get_id() == target_id:
                return path

            for _, vertex in enumerate(v.get_neighbors()):
                # add vertex to stack
                if vertex.get_id() not in visited:
                    stack.append(vertex.get_id())
                    visited.add(vertex.get_id())

        return list()

    def contains_dfs(self, start_vertex, path):

        # add current vertex to path
        path.add(start_vertex.get_id())

        for index, vertex in enumerate(start_vertex.get_neighbors()):
            # base case, cycle is found
            if vertex.get_id() in path:
                return True
            # vertex not in path - call dfs
            else:
                # add id to path
                path.add(vertex.get_id())
                # recurse deeper, make sure a true result returns properly
                return self.contains_dfs(vertex, path)
                # remove from path once dfs call finishes
                path.remove(vertex.get_id())

            # print(f'Current path: {path}')
        return False

    def dfs_recursive(self, start_id):
        """Visit each vertex, starting with start_id, in DFS order."""

        visited = set()  # set of vertices we've visited so far
        visited.add(start_id)

        start_vertex = self.get_vertex(start_id)
        self.contains_dfs(start_vertex, visited)

    def contains_cycle(self):
        """
        Check if a graph contains a cycle
        """
        path = set()

        start_vertex = self.get_vertices()[0]

        return self.contains_dfs(start_vertex, path)

    def topo_dfs(self, start_vertex, visited):
        visited.add(start_vertex.get_id())
        for _, vertex in enumerate(start_vertex.get_neighbors()):
            if vertex.get_id() not in visited:
                self.topo_dfs(vertex, visited)

    def topological_sort(self):
        """
        Return a valid ordering of vertices in a directed acyclic graph.
        If the graph contains a cycle, throw a ValueError.
        """

        if self.contains_cycle():
            raise ValueError(self)
        visited = set()
        stack = deque()
        for _, vertex in enumerate(self.get_vertices()):
            self.topo_dfs(vertex, visited)

            stack.append(vertex.get_id())

        # extra cheese :))))
        item = stack.pop()
        stack.appendleft(item)
        return list(stack)
