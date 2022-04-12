import copy


class Graph:

    def __init__(self):
        self._vertices_in = {}
        self._vertices_out = {}
        self._edges = {}
        self._number_vertices = 0
        self._number_edges = 0

    @property
    def vertices_in(self):
        return self._vertices_in

    @property
    def vertices_out(self):
        return self._vertices_out

    @property
    def edges(self):
        return self._edges

    def add_vertex_in(self, vertex_in, vertex_out):
        self._vertices_in[vertex_in].append(vertex_out)

    def add_vertex_out(self, vertex_out, vertex_in):
        self._vertices_out[vertex_out].append(vertex_in)

    def read_edge(self, origin, end, cost):
        self._edges[(origin, end)] = cost

    def add_edge(self, origin, end, cost):
        if origin in list(self._vertices_out.keys()) and end in list(self._vertices_out.keys()):
            pair = (origin, end)
            if pair not in self._edges:
                self._edges[pair] = cost
                self.add_vertex_in(end, origin)
                self.add_vertex_out(origin, end)
                self._number_edges = self._number_edges + 1
                return True
            else:
                return False
        else:
            return False

    def add_empty_vertex(self, vertex):
        if vertex not in self._vertices_in:
            self._vertices_in[vertex] = []
            self._number_vertices = self._number_vertices + 1
            self._vertices_out[vertex] = []
        else:
            print("This vertex exists already")

    @property
    def number_vertices(self):
        return self._number_vertices

    @property
    def number_edges(self):
        return self._number_edges

    @number_vertices.setter
    def number_vertices(self, value):
        self._number_vertices = value

    @number_edges.setter
    def number_edges(self, value):
        self._number_edges = value

    def vertices_set(self):
        return list(self._vertices_out.keys())

    def edges_set(self):
        return list(self._edges.keys())

    def search_edge(self, origin, end):
        if origin in list(self._vertices_out.keys()):
            for i in self._vertices_out[origin]:
                if i == end:
                    return True
        return False

    def remove_vertex(self, vertex):
        if vertex in list(self._vertices_out.keys()):
            for i in list(self._vertices_out.keys()):
                if vertex in self._vertices_in[i]:
                    self._vertices_in[i].remove(vertex)
                if vertex in self.vertices_out[i]:
                    self._vertices_out[i].remove(vertex)
            del self._vertices_in[vertex]
            del self._vertices_out[vertex]
            self._number_vertices = self._number_vertices - 1
            k = 0
            for pair in self._edges.copy():
                if pair[0] == vertex or pair[1] == vertex:
                    del self._edges[pair]
                    k = k+1
            self._number_edges = self._number_edges - k
        else:
            print("This vertex does not exist.")

    def remove_edge(self, origin, end):
        condition = self.search_edge(origin, end)
        pair = (origin, end)
        if condition:
            del self._edges[pair]
            self._vertices_in[end].remove(origin)
            self._vertices_out[origin].remove(end)
        else:
            print("This edge does not exist")

    def change_cost(self, origin, end, cost):
        condition = self.search_edge(origin, end)
        pair = (origin, end)
        if condition:
            self._edges[pair] = cost
        else:
            print("This edge does not exist")

    def in_degree_vertex(self, vertex):
        if vertex in self._vertices_in.keys():
            return len(self._vertices_in[vertex])
        else:
            print("This vertex does not exist.")
            return -1

    def out_degree_vertex(self, vertex):
        if vertex in self._vertices_out.keys():
            return len(self._vertices_out[vertex])
        else:
            print("This vertex does not exist.")
            return -1

    def outbound_edges(self, vertex):
        if vertex in self._vertices_out.keys():
            return self._vertices_out[vertex]
        else:
            print("This vertex does not exist.")
            return -1

    def inbound_edges(self, vertex):
        if vertex in self._vertices_in.keys():
            return self._vertices_in[vertex]
        else:
            print("This vertex does not exist.")
            return -1

    def get_cost(self, origin, end):
        condition = self.search_edge(origin, end)
        pair = (origin, end)
        if condition:
            return self._edges[pair]
        else:
            print("This edge does not exist")
            return False

    def copy_graph(self):
        g = Graph()
        g = copy.deepcopy(self)
        return g
