from graphs.graph import Graph


def read_graph_from_file(filename):
    """
    Read in data from the specified filename, and create and return a graph
    object corresponding to that data.

    Arguments:
    filename (string): The relative path of the file to be processed

    Returns:
    Graph: A directed or undirected Graph object containing the specified
    vertices and edges
    """

    # TODO: Use 'open' to open the file
    with open(filename) as f:
        line = f.readline()
        # read first line
        if line == 'G':
            g = Graph(is_directed=False)
        else:
            g = Graph()

        # read second line and split it into a comma and add vertices
        line = f.readline()
        vertices = f.readline().split(',')
        for _, v in enumerate(vertices):
            g.add_vertex(v)

        # add edges
        line = f.readline()
        while line:
            vertex = line.strip('()').split(',')
            g.add_edge(vertex[0], vertex[1])
            line = f.readline()


if __name__ == '__main__':

    graph = read_graph_from_file('test.txt')
    print(graph)
