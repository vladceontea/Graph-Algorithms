import random

from Graph import Graph
from queue import PriorityQueue
from dataclasses import dataclass


@dataclass
class Activity:
    """
    The representation of the activities from the table
    """
    name: str
    value: int
    dur: int
    time_early_start: int
    time_early_end: int
    time_late_start: int
    time_late_end: int


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
    print("17. Read a list of activities and create its associated graph.")
    print("18. Verify if a graph is a DAG.")
    print("19. Find the starting time of the activities, the total time of a project and its critical activities.")
    print("20. Get the minimum cost Hamiltonian cycle.")
    print("0. Exit")
    print("\n")


def modify_menu():
    print("1. Add vertex")
    print("2. Add edge")
    print("3. Remove a vertex")
    print("4. Remove an edge")


def read_activities():
    """
    Reads the table and creates a directed graph based on it
    """
    graph = Graph()
    file = input("Enter file name:")
    f = open(file, 'rt')
    lines = f.readlines()
    f.close()
    i = 1
    activities = [(Activity("START", 0, 0, 0, 0, 0, 0))]
    graph.add_empty_vertex(0)
    for line in lines:
        line = line.split(' ')
        if len(line) == 2:
            activities.append(Activity(line[0], i, int(line[1]), 0, 0, 0, 0))
            graph.add_empty_vertex(i)
            graph.add_vertex_out(0, i)
            graph.add_vertex_in(i, 0)
            graph.read_edge(0, 1, 0)
        elif len(line) > 2:
            activities.append(Activity(line[0], i, int(line[1]), 0, 0, 0, 0))
            graph.add_empty_vertex(i)
            for j in range(len(line) - 2):
                if j == len(line) - 3:
                    newstr = line[j + 2].replace("\n", "")
                    k = 0
                    for k in range(len(activities)):
                        if newstr == activities[k].name:
                            break
                    graph.add_vertex_in(activities[i].value, activities[k].value)
                    graph.add_vertex_out(activities[k].value, activities[i].value)
                    graph.read_edge(activities[k].value, activities[i].value, activities[k].dur)
                else:
                    k = 0
                    for k in range(len(activities)):
                        if line[j + 2] == activities[k].name:
                            break
                    graph.add_vertex_in(activities[i].value, activities[k].value)
                    graph.add_vertex_out(activities[k].value, activities[i].value)
                    graph.read_edge(activities[k].value, activities[i].value, activities[k].dur)

        i = i + 1

    activities.append(Activity("END", i, 0, 0, 0, 0, 0))
    graph.add_empty_vertex(i)
    x = 0
    while x < i:
        if not graph.vertices_out[x]:
            graph.add_vertex_out(x, i)
            graph.add_vertex_in(i, x)
            graph.read_edge(x, i, activities[x].dur)
        x = x + 1

    return graph, activities


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

    if n * n < m:
        print("The number of edges given is over the possible number of edges for this graph. Will create only " + str(
            n * n) + " edges.")
        remaining_edges = n * n

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
        print("x = " + str(x))
        for y in graph.vertices_out[x]:
            if y not in dist_dict.keys() or dist_dict[x] + graph.get_cost(x, y) < dist_dict[y]:
                dist_dict[y] = dist_dict[x] + graph.get_cost(x, y)
                q.put((dist_dict[y], y))
                prev_dict[y] = x
        if x == t:
            found = True

    walk = []
    cost = 0
    print(dist_dict)
    if found:
        walk.append(t)
        while walk[-1] != s:
            walk.append(prev_dict[walk[-1]])
        walk.reverse()
        cost = dist_dict[t]

    return walk, cost


def topological_sort_dfs(graph, x, sorted_list, fully_process, in_process):
    """
    An additional function used to help in the topological sorting
    graph - the directed graph
    x - the node that is currently processed
    sorted_list - the list of the topological sorting
    fully_process - the set of nodes processed
    in_process - the set of nodes that are currently processing
    """
    in_process.add(x)
    print("x = " + str(x))
    for y in graph.vertices_in[x]:
        print("y = " + str(y))
        if y in in_process:
            return False
        elif y not in fully_process:
            ok = topological_sort_dfs(graph, y, sorted_list, fully_process, in_process)
            if not ok:
                return False

    in_process.remove(x)
    sorted_list.append(x)
    fully_process.add(x)
    return True


def topological_sort(graph):
    """
    Checks if the graph is a DAG and if so, returns its topological sorting
    graph - the directed graph
    """
    sorted_list = []
    fully_process = set()
    in_process = set()
    for x in graph.vertices_in:
        if x not in fully_process:
            ok = topological_sort_dfs(graph, x, sorted_list, fully_process, in_process)
            if not ok:
                return []

    return sorted_list


def choose(graph, last, visited):
    """
    Chooses the next vertex by finding the shortest path from the current one
    graph - the directed graph
    last - the vertex from where we choose the shortest path
    visited - the set of vertices already in the path
    """
    minim = 10000
    j_min = -1
    for j in graph.vertices_out[last]:
        if visited[j] != 1:
            if graph.get_cost(last, j) < minim:
                minim = graph.get_cost(last, j)
                j_min = j
    return minim, j_min


def hamiltonian_cycle(graph):
    """
    Finds the minimum cost Hamiltonian cycle (if there is one)
    graph - the directed graph
    """
    save_cost = 10000
    save_path = []

    for index in range(0, graph.number_vertices):
        visited = [0] * graph.number_vertices
        path = [index]
        visited[index] = 1
        cost = 0
        i = 0
        j_min = 10000
        while i < graph.number_vertices-1 and j_min != -1:
            minim, j_min = choose(graph, path[- 1], visited)
            path.append(j_min)
            visited[j_min] = 1
            cost = cost + minim
            i = i + 1

        if j_min == -1:
            cost = save_cost
        elif graph.search_edge(path[graph.number_vertices - 1], index):
            cost = cost + graph.get_cost(path[graph.number_vertices - 1], index)
        else:
            cost = save_cost

        if cost < save_cost:
            save_path = []
            for i in range(0, graph.number_vertices):
                save_path.append(path[i])
            save_cost = cost
            save_path.append(save_path[0])

    return save_path, save_cost


def start():
    graph = Graph()
    activities = []
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

        elif option == 17:
            graph, activities = read_activities()

        elif option == 18:
            dag = topological_sort(graph)

            if len(dag) == 0:
                print("This graph is not a DAG.")
            else:
                print("The topological sorting is:")
                print(*dag)

        elif option == 19:
            dag = topological_sort(graph)

            if len(dag) == 0:
                print("This graph is not a DAG.")
            else:
                my_list = []
                for x in dag:
                    my_list.append(activities[x].name)
                print("The topological sorting is:")
                print(*my_list)

                for v in dag:
                    if v > 0:
                        k = 0
                        for w in graph.vertices_in[v]:
                            if k == 0:
                                activities[v].time_early_start = activities[w].time_early_end
                                k = 1
                            elif activities[v].time_early_start < activities[w].time_early_end:
                                activities[v].time_early_start = activities[w].time_early_end
                        activities[v].time_early_end = activities[v].time_early_start + activities[v].dur

                activities[v].time_late_end = activities[v].time_early_end
                activities[v].time_early_start = activities[v].time_late_end - activities[v].dur
                dag.reverse()
                for v in dag:
                    if v < len(dag):
                        k = 0
                        for w in graph.vertices_out[v]:
                            if k == 0:
                                activities[v].time_late_end = activities[w].time_late_start
                                k = 1
                            elif activities[v].time_late_end > activities[w].time_late_start:
                                activities[v].time_late_end = activities[w].time_late_start
                        activities[v].time_late_start = activities[v].time_late_end - activities[v].dur

                dag.reverse()
                critical = []
                for v in dag:
                    if activities[v].time_early_start == activities[v].time_late_start:
                        critical.append(activities[v].name)
                print()
                v = 0
                for x in my_list:
                    print("The earliest start time for activity " + x + " is " + str(activities[v].time_early_start))
                    v = v + 1
                print()
                v = 0
                for x in my_list:
                    print("The latest start time for activity " + x + " is " + str(activities[v].time_late_start))
                    v = v + 1
                print()
                print("The critical activities are:")
                print(*critical)

                print("The total time of the project is: ")
                print(activities[len(dag) - 1].time_late_start)

        elif option == 20:
            path, cost = hamiltonian_cycle(graph)
            if len(path) == 0:
                print("There is no Hamiltonian cycle in the graph")
            else:
                print("The cost of the cycle is: " + str(cost))
                print("The cycle is: ")
                print(*path)

        elif option == 0:
            ok = 0


start()
