import random

from Graph import Graph
from queue import PriorityQueue


def main_menu():
    print("\n")
    print("1. Read a graph from file")
    print("2. Modify the graph.")
    print("3. Change the cost of an edge")
    print("4. Show number of vertices")
    print("5. Show number of edges")
    print("6. See the vertices.")
    print("7. Search for an edge")
    print("8. Get the in degree and the out degree of a vertex.")
    print("9. See the outbound edges of a vertex.")
    print("10. See the inbound edges of a vertex.")
    print("11. Copy the graph.")
    print("12. Write the graph in a file.")
    print("13. Generate a random graph.")
    print("14. Get the cost of an edge")
    print("15. Find the minimum length path between two vertices.")
    print("16. Find the lowest cost walk between two vertices.")
    print("0. Exit")
    print("\n")


def modify_menu():
    print("1. Add vertex")
    print("2. Add edge")
    print("3. Remove a vertex")
    print("4. Remove an edge")


def read_graph():

    graph = Graph()
    file = input("Enter file name:")
    f = open(file, 'rt')
    lines = f.readlines()
    f.close()

    for line in lines:
        line = line.split(' ')
        if len(line) == 2:
            number_vertices = int(line[0])
            graph.number_edges = int(line[1])
            for i in range(number_vertices):
                graph.add_empty_vertex(i)
        if len(line) == 3:
            newstr = line[2].replace("\n", "")
            graph.add_vertex_in(int(line[1]), int(line[0]))
            graph.add_vertex_out(int(line[0]), int(line[1]))
            graph.read_edge(int(line[0]), int(line[1]), int(newstr))
    return graph


def write_graph(graph):
    file = input("Enter file name:")
    f = open(file, 'wt')

    try:
        first_line = str(graph.number_vertices) + " " + str(graph.number_edges)
        f.write(first_line)
        f.write("\n")
        for pair in graph.edges:
            edge_str = str(pair[0]) + " " + str(pair[1]) + " " + str(graph.edges[pair])
            f.write(edge_str)
            f.write("\n")
        f.close()
    except Exception as e:
        print("An error occurred -" + str(e))


def generate_graph(n, m):
    g = Graph()
    number_vertices = n
    g.number_edges = 0
    remaining_edges = m
    for i in range(number_vertices):
        g.add_empty_vertex(i)

    if n*n < m:
        print("The number of edges given is over the possible number of edges for this graph. Will create only " + str(n*n) + " edges.")
        remaining_edges = n*n

    while remaining_edges > 0:
        x = random.randrange(n)
        y = random.randrange(n)
        c = random.randrange(50)

        if g.add_edge(x, y, c):
            remaining_edges = remaining_edges - 1

    return g


def find_minimum_length_path(graph, s, t):
    """
    Using a backward BFS, this algorithm computes the path between two vertices and its length (if there is a possible path)
    s - source vertex
    t - end vertex
    graph - the directed graph
    """
    dist_dict = {}
    next_dict = {}
    visited_set = {t}
    queue = [t]
    dist_dict[t] = 0
    path = []
    ok = 0
    while len(queue) > 0:
        x = queue.pop(0)
        for y in graph.vertices_in[x]:
            if y not in visited_set:
                queue.append(y)
                visited_set.add(y)
                dist_dict[y] = dist_dict[x] + 1
                next_dict[y] = x
            if y == s:
                ok = 1
                break
        if ok == 1:
            break

    length = 0
    if s in visited_set:
        path.append(s)
        while path[-1] != t:
            path.append(next_dict[path[-1]])
        length = dist_dict[s]
    return path, length


def find_lowest_cost_walk(graph, s, t):
    """
    Given a directed graph, find the lowest cost walk between two vertices using Dijkstra's algorithm
    s - source vertex
    t - end vertex
    graph - the directed graph
    """
    prev_dict = {}
    dist_dict = {}
    q = PriorityQueue()
    q.put((0, s))
    dist_dict[s] = 0
    found = False
    while not q.empty() and not found:
        x = q.get()[1]
        for y in graph.vertices_out[x]:
            if y not in dist_dict.keys() or dist_dict[x] + graph.get_cost(x, y) < dist_dict[y]:
                dist_dict[y] = dist_dict[x] + graph.get_cost(x, y)
                q.put((dist_dict[y], y))
                prev_dict[y] = x
        if x == t:
            found = True

    walk = []
    cost = 0
    if found:
        walk.append(t)
        while walk[-1] != s:
            walk.append(prev_dict[walk[-1]])
        walk.reverse()
        cost = dist_dict[t]

    return walk, cost


def start():

    graph = Graph()
    copy_graph = Graph()
    ok = 1
    while ok == 1:
        main_menu()
        option = int(input("Enter command: "))
        if option == 1:
            graph = read_graph()

        elif option == 2:
            modify_menu()
            option = int(input("Enter command: "))

            if option == 1:
                vertex = int(input("Enter the vertex name: "))
                graph.add_empty_vertex(vertex)

            elif option == 2:
                if graph.number_vertices == 0:
                    print("No graph exists")
                else:
                    origin = int(input("Enter the name of the origin vertex: "))
                    end = int(input("Enter the name of the end vertex: "))
                    cost = int(input("Enter the cost of the edge: "))
                    if not graph.add_edge(origin, end, cost):
                        print("Cannot create this edge.")

            elif option == 3:
                if graph.number_vertices == 0:
                    print("No graph exists")
                else:
                    vertex = int(input("Enter the vertex name: "))
                    graph.remove_vertex(vertex)

            elif option == 4:
                if graph.number_vertices == 0:
                    print("No graph exists")
                else:
                    origin = int(input("Enter the name of the origin vertex: "))
                    end = int(input("Enter the name of the end vertex: "))
                    graph.remove_edge(origin, end)

        elif option == 3:
            origin = int(input("Enter the name of the origin vertex: "))
            end = int(input("Enter the name of the end vertex: "))
            cost = int(input("Enter the new cost of the edge: "))
            graph.change_cost(origin, end, cost)

        elif option == 4:
            if graph.number_vertices == 0:
                print("No graph exists")
            else:
                print(graph.number_vertices)

        elif option == 5:
            if graph.number_vertices == 0:
                print("No graph exists")
            else:
                print(graph.number_edges)

        elif option == 6:
            vertices_set = graph.vertices_set()
            if vertices_set:
                print("The vertices are: ")
                print(*vertices_set)
            else:
                print("No graph exists")

        elif option == 7:
            origin = int(input("Enter the name of the origin vertex: "))
            end = int(input("Enter the name of the end vertex: "))
            answer = graph.search_edge(origin, end)
            if answer:
                print("This edge exists")
            else:
                print("This edge does not exist.")

        elif option == 8:
            vertex = int(input("Enter the vertex name: "))
            in_degree = graph.in_degree_vertex(vertex)
            out_degree = graph.out_degree_vertex(vertex)

            if in_degree != -1 and out_degree != -1:
                print("The in degree is: " + str(in_degree))
                print("The out degree is: " + str(out_degree))

        elif option == 9:
            vertex = int(input("Enter the vertex name: "))
            out_edges = graph.outbound_edges(vertex)
            if out_edges != -1:
                if len(out_edges) == 0:
                    print("No outbound edges.")
                else:
                    print(*out_edges)

        elif option == 10:
            vertex = int(input("Enter the vertex name: "))
            in_edges = graph.inbound_edges(vertex)
            if in_edges != -1:
                if len(in_edges) == 0:
                    print("No inbound edges.")
                else:
                    print(*in_edges)

        elif option == 11:
            copy_graph = graph.copy_graph()

        elif option == 12:
            write_graph(graph)

        elif option == 13:
            n = int(input("Enter the number of vertices: "))
            m = int(input("Enter the number of edges: "))
            graph = generate_graph(n, m)

        elif option == 14:
            origin = int(input("Enter the name of the origin vertex: "))
            end = int(input("Enter the name of the end vertex: "))

            cost = graph.get_cost(origin, end)
            if cost:
                print(cost)

        elif option == 15:
            s = int(input("Enter the first vertex: "))
            t = int(input("Enter the second vertex: "))

            path, min_length = find_minimum_length_path(graph, s, t)
            if len(path) == 0:
                print("No path between these two vertices.")
            else:
                print("The path is: ")
                print(*path)
                print("The length of the path is: ")
                print(min_length)

        elif option == 16:
            s = int(input("Enter the first vertex: "))
            t = int(input("Enter the second vertex: "))

            walk, min_cost = find_lowest_cost_walk(graph, s, t)
            if len(walk) == 0:
                print("No walk between these two vertices.")
            else:
                print("The walk is: ")
                print(*walk)
                print("The cost of the walk is: ")
                print(min_cost)

        elif option == 0:
            ok = 0


start()
