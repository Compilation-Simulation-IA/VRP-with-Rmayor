from queue import Queue


class Node:
    """
    Represents the nodes of class Graph. Stores the number (or name) of the node as string or number.
    Edges are stored like [node, costs] to implement both weighted and unweighted graphs.
    ATTENTION: edge-nodes are now stored as objects!
    """

    def __init__(self, name):
        self.__name = name  # name/number of the node
        self.__adjacent_nodes = []
        self.__marked = False

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def unmark(self):
        self.__marked = False

    def is_marked(self):
        return self.__marked

    def mark(self):
        self.__marked = True

    def add_adjacent_node(self, new_node, costs):
        for node in self.__adjacent_nodes:
            if node[0].get_name() == new_node.get_name():
                return False
        self.__adjacent_nodes.append([new_node, costs])
        return True

    def has_adjacent_node(self, node_number):

        """
        @param node_number: Node name (as a string) that will be checked.
        @return: Whether the node has an edge leading to the given node or not.
        """

        for node in self.__adjacent_nodes:
            if node[0].get_name() == node_number:
                return True
        return False

    def get_edge_cost(self, target_node):

        """
        Returns the cost for edge node-target_node.
        @param target_node: Name of the target node as a string.
        @return: Cost of edge node-target_node.
        """

        if target_node in self.get_adjacent_nodes_numbers():
            cost = [edge[1] for edge in self.__adjacent_nodes if edge[0].get_name() == target_node][0]
            return cost
        return float('inf')

    def get_adjacent_nodes(self):
        return self.__adjacent_nodes

    def get_adjacent_nodes_numbers(self):
        return [node[0].get_name() for node in self.__adjacent_nodes]

    def set_adjacent_nodes(self, nodes):
        self.__adjacent_nodes = nodes


class Graph:
    """
    Represents a graph-object. Stores the nodes, as well as a node-counter which represents the graph's size.
    Other class-variables ("self.__dfs_content" and "self.__marked_nodes") are used in several class-methods.
    The class "Graph" serves plenty of methods, such as adding and deleting nodes, setting edges, calculating shortest
    paths, etc.
    """

    def __init__(self):
        self.__nodes = []
        self.__dfs_content = dict()
        self.__dfs_time = 0
        self.__count_nodes = 0
        self.__current_fw_table = None

    def find_node(self, node_number):
        for node in self.__nodes:
            if node.get_name() == node_number:
                return node
        return None

    def add_node(self, name):
        self.__nodes.append(Node(name))
        self.__count_nodes += 1
        self.__current_fw_table = self.__floyd_warshall()

    def unmark_all_nodes(self):
        for node in self.__nodes:
            node.unmark()

    def set_edge(self, first_node_number, second_node_number, directed, costs=1):
        if first_node_number != '' and second_node_number != '':
            first_node = self.find_node(first_node_number)
            second_node = self.find_node(second_node_number)
            if first_node is not None and second_node is not None:
                first_node.add_adjacent_node(second_node, costs)
                if not directed:
                    second_node.add_adjacent_node(first_node, costs)
                self.__current_fw_table = self.__floyd_warshall()
                return True
        return False

    def remove_node(self, node_number):
        node_delete = self.find_node(node_number)
        if node_delete is not None:
            self.__nodes.remove(node_delete)
            for node in self.__nodes:
                edge_buffer = node.get_adjacent_nodes()
                for index in range(len(edge_buffer)):
                    if edge_buffer[index][0].get_name() == node_delete.get_number():
                        edge_buffer.pop(index)
                        self.__count_nodes -= 1
                        break
                node.set_adjacent_nodes(edge_buffer)
            self.__current_fw_table = self.__floyd_warshall()
            return True
        return False

    def __iter__(self):
        self.__counting_variable = 0
        return self

    def __next__(self):
        if self.__counting_variable < self.__count_nodes:
            self.__counting_variable += 1
            return self.__nodes[self.__counting_variable - 1]
        else:
            raise StopIteration

    def breadth_first_search(self, starting_node):

        """
        Returns the result of breadth-first-search as a list like [node, predecessor, costs].
        @param starting_node: Indicates the starting node. The BFS starts here. Represented by a string or number.
        @return: Returns BFS result as [node, predecessor, distance-level].
        """

        self.unmark_all_nodes()
        source_node = self.find_node(starting_node)
        if not starting_node:
            return []
        bfs_list = []
        queue = Queue()
        source_node.mark()
        queue.put([source_node, None, 0])
        while not queue.empty():
            element = queue.get()
            bfs_list.append([element[0].get_name(), element[1], element[2]])
            for edge in element[0].get_adjacent_nodes():
                if not edge[0].is_marked():
                    edge[0].mark()
                    queue.put([edge[0], element[0].get_name(), element[2] + 1])
        return bfs_list

    def depth_first_search(self):

        """
        Calculates the result of DFS and returns a dictionary as {node: [predecessor, starting-time, finishing-time], ...}.
        Uses "__dfs_visit()" to step through the nodes.
        @return: Result of DFS as {node: [predecessor, starting-time, finishing-time], ...}.
        """

        self.unmark_all_nodes()
        self.__dfs_time = 0
        self.__dfs_content = dict()
        for node in self.__nodes:
            if not node.is_marked():
                self.__dfs_visit(node.get_name(), None)
        return self.__dfs_content

    def __dfs_visit(self, node_number, predecessor):
        self.find_node(node_number).mark()
        starting_time = self.__dfs_time
        self.__dfs_time += 1
        for node in self.find_node(node_number).get_adjacent_nodes():
            if not node[0].is_marked():
                self.__dfs_visit(node[0].get_name(), node_number)
        self.__dfs_content[node_number] = [predecessor, starting_time, self.__dfs_time]
        self.__dfs_time += 1

    def topological_sort(self):

        """
        Calculates a topological sorting of the vertices.
        @return: Returns a list, in which all vertices are sorted topologically.
        """

        dfs_result = self.depth_first_search()
        topological_sort = [[key, dfs_result[key][2]] for key in dfs_result.keys()]
        topological_sort.sort(key=lambda x: x[1], reverse=True)
        return topological_sort

    def __construct_dijkstra_table(self, source_node):

        """
        Constructs the initial Dijkstra-table for node "start".
        @param source_node: Starting node. Table will be constructed with costs for start set to 0.
        @return: Returns the initial Dijkstra-table as a dictionary with entries like {"Name": costs, ...}.
        """

        dijkstra_table = dict()
        for node in self.__nodes:
            if node.get_name() != source_node:
                dijkstra_table[node.get_name()] = [float('inf'), None]
            else:
                dijkstra_table[node.get_name()] = [0, None]
        return dijkstra_table

    def __find_cheapest_node(self, nodes, dijkstra_table):

        """
        Finds the cheapest non-visited node in the Dijkstra-table.
        @param nodes: List of nodes represented by a string or number.
        @param dijkstra_table: Current Dijkstra-table.
        @return: Returns the cheapest non-visited node as a node-object.
        """

        if nodes:
            cheapest_node = [float('inf'), nodes[0]]
            for key in dijkstra_table.keys():
                if key in nodes and dijkstra_table[key][0] < cheapest_node[0]:
                    cheapest_node = [dijkstra_table[key][0], key]
            return self.find_node(cheapest_node[1])
        return None

    def __construct_shortest_path(self, source_node, target_node, table):

        """
        Constructs the shortest path according to the Dijkstra-table.
        @param source_node: Starting node represented by a string or number.
        @param target_node: Ending node represented by a string or number.
        @param table: The Dijkstra-table or the Bellman-Ford-table that was calculated by "__shortest_path()"
                        or "__shortest_path_bf()".
        @return: Constructs the shortest path according to the table and returns it as a list.
        """

        if table[target_node][0] == float('inf'):
            return []
        current_node = target_node
        path = []
        while current_node != source_node:
            path.insert(0, [current_node, str(table[current_node][0])])
            current_node = table[current_node][1]
        path.insert(0, [source_node, '0'])
        return path

    def __shortest_path(self, source_node):

        """
        NOTE: Edges have to be stored like [node, costs], where "node" is an object.
        Calculates the shortest path between start and end using the Dijkstra-algorithm.
        @param source_node: The first node of the shortest path. Path starts there. Has to be a string or a number!
        @return: Returns the Dijkstra-table that was calculated.
        """

        dijkstra_table = self.__construct_dijkstra_table(source_node)
        nodes = [node.get_name() for node in self.__nodes]
        current_node = self.find_node(source_node)
        while nodes:
            for node in current_node.get_adjacent_nodes():  # Note: edges are stored like [node, costs]
                if dijkstra_table[current_node.get_name()][0] + node[1] < dijkstra_table[node[0].get_name()][0]:
                    dijkstra_table[node[0].get_name()][0] = dijkstra_table[current_node.get_name()][0] + node[1]
                    dijkstra_table[node[0].get_name()][1] = current_node.get_name()
            nodes.remove(current_node.get_name())
            current_node = self.__find_cheapest_node(nodes, dijkstra_table)
        return dijkstra_table

    def get_shortest_path(self, source_node, target_node, mode):

        """
        NOTES: Edges have to be stored like [node, costs], where "node" is an object.
        Calculates the shortest path between start and end using the Dijkstra-/Bellman-Ford-algorithm.
        Calculates the cost of the shortest path by using the Floyd-Warshall-algorithm.
        @param source_node: The first node of the shortest path. Path starts there. Has to be a string or a number!
        @param target_node: The last node of the shortest path. Path ends here. Has to be a string or a number!
        @param mode: Use 'bf' (Bellman-Ford), 'dij' (Dijkstra) or 'fw' (Floyd-Warshall) to choose the algorithm.
        @return: Returns the shortest path according to the calculated Dijkstra-/Bellman-Ford-table as a list.
        """
        if mode == 'bf':
            return self.__construct_shortest_path(source_node, target_node, self.__shortest_path_bf(source_node))
        elif mode == "dij":
            return self.__construct_shortest_path(source_node, target_node, self.__shortest_path(source_node))
        elif mode == "fw":
            return self.__construct_shortest_path_fw(source_node, target_node, self.__current_fw_table)
        print("Invalid mode. Use 'bf' or 'dij' to select an algorithm.")
        return None

    def __construct_bf_table(self, source_node):

        """
        Constructs the initial table for the Bellman-Ford-algorithm.
        @param source_node: The name of the source node as a string.
        @return: Returns the initial Bellman-Ford-table for further usage.
        """

        bf_table = dict()
        source_node: Node = self.find_node(source_node)
        for node in self.__nodes:
            if node.get_name() == source_node.get_name():
                bf_table[node.get_name()] = [0, None]
            elif source_node.has_adjacent_node(node.get_name()):
                bf_table[node.get_name()] = [source_node.get_edge_cost(node.get_name()), source_node.get_name()]
            else:
                bf_table[node.get_name()] = [float('inf')]
        return bf_table

    def __shortest_path_bf(self, source_node):

        """
        NOTE: Edges have to be stored like [node, costs], where "node" is an object.
        Calculates the final Bellman-Ford-table from source_node to all other nodes.
        @param source_node: The source_node's name as a string.
        @return: Returns the final Bellman-Ford-table.
        """

        bf_table = self.__construct_bf_table(source_node)
        for _ in range(self.__count_nodes - 1):
            changed = False
            for node in self.__nodes:
                for edge in node.get_adjacent_nodes():
                    if bf_table[node.get_name()][0] + edge[1] < bf_table[edge[0].get_name()][0]:
                        bf_table[edge[0].get_name()] = [bf_table[node.get_name()][0] + edge[1], node.get_name()]
                        changed = True
            if not changed:
                break
        return bf_table

    def __construct_shortest_path_fw(self, source_node, target_node, fw_table):

        """
        Constructs the shortest path between two vertices.
        @param source_node: The source node's name.
        @param target_node: The target node's name.
        @param fw_table:  The final FLoyd-Warshall-table.
        @return: Returns the costs and the shortest path between the two vertices like [cost, node1, ..., node_n].
        """

        current_node = source_node
        path = [fw_table[source_node][target_node][0], current_node]
        while current_node != target_node:
            current_node = fw_table[current_node][target_node][1]
            path.append(current_node)
        return path

    def __construct_fw_table(self):

        """
        Constructs the table for the Floyd-Warshall-algorithm.
        Table is built like {node_name: {node1: [cost1, next_1], ..., node_n: [cost_n, next_n]}, ...}.
        Table and sub-tables include all nodes, since Floyd-Warshall is an all-pair-algorithm.
        @return: Returns the table in form of a dictionary.
        """

        fw_table = dict()
        for node in self.__nodes:
            fw_table[node.get_name()] = dict()
            for target_node in self.__nodes:
                if node.get_name() == target_node.get_name():
                    fw_table[node.get_name()][node.get_name()] = [0, node.get_name()]
                else:
                    if node.has_adjacent_node(target_node.get_name()):
                        fw_table[node.get_name()][target_node.get_name()] = \
                            [node.get_edge_cost(target_node.get_name()), target_node.get_name()]
                    else:
                        fw_table[node.get_name()][target_node.get_name()] = [float('inf'), None]
        return fw_table

    def __floyd_warshall(self):

        """
        Calculates all shortest paths using Floyd-Warshall-algorithm.
        @return: Returns the final Floyd-Warshall-table with all shortest paths.
        """

        fw_table = self.__construct_fw_table()
        for node_k in self.__nodes:
            for node_i in self.__nodes:
                for node_j in self.__nodes:
                    if fw_table[node_i.get_name()][node_j.get_name()][0] > \
                            fw_table[node_i.get_name()][node_k.get_name()][0] + \
                            fw_table[node_k.get_name()][node_j.get_name()][0]:
                        fw_table[node_i.get_name()][node_j.get_name()][0] = \
                            fw_table[node_i.get_name()][node_k.get_name()][0] + \
                            fw_table[node_k.get_name()][node_j.get_name()][0]
                        fw_table[node_i.get_name()][node_j.get_name()][1] = \
                            fw_table[node_i.get_name()][node_k.get_name()][1]
        return fw_table


if __name__ == "__main__":
    g = Graph()
    g.add_node('x')
    g.add_node('y')
    g.add_node('z')
    g.add_node('u')
    g.add_node('v')
    g.add_node('w')
    g.set_edge('x', 'y', True, 2)
    g.set_edge('x', 'w', True, -1)
    g.set_edge('y', 'x', True, 5)
    g.set_edge('y', 'z', True, 1)
    g.set_edge('z', 'u', True, 3)
    g.set_edge('z', 'w', True, -2)
    g.set_edge('u', 'v', True, 7)
    g.set_edge('v', 'u', True, 2)
    g.set_edge('w', 'x', True, 3)
    print(g.get_shortest_path('x', 'v', 'fw'))