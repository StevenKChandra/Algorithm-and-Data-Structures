def Djikstra_Algortihm(graph, source):
    
    def _initialize ():
        nonlocal graph, source, vertex_count
        d = {}
        p = {}
        for vertex in range(vertex_count):
            d[vertex] = float("inf")
            p[vertex] = []
        d[source] = 0
        return d, p
    
    def _weightmatrix(graph):
        nonlocal vertex_count
        if vertex_count == len(graph[0]) and (isinstance(graph[0][0], int) or isinstance(graph[0][0], float)):
           return graph
        else:
            weight = [[float("inf") for i in range(vertex_count)] for y in range(vertex_count)]
            for source in range (vertex_count):
                for destination, weight in graph[source]:
                    weight[source][destination] = weight
                weight [source][source] = 0
            return weight
    
    def _relax(source, destination):
        nonlocal distance, path, weight, Q
        new_distance = distance[source] +  weight[source][destination]
        if distance[destination] > new_distance:
            distance[destination] = new_distance
            path[destination] = path[source] + [source]
            Q.insert(new_distance, destination)
    
    from Data_Structures import PriorityQueue, RedBlackTree
    
    vertex_count = len(graph)
    distance, path = _initialize()
    weight = _weightmatrix(graph)
    S = RedBlackTree()
    Q = PriorityQueue()

    for vertex in range(vertex_count):
        Q.insert(distance[vertex], vertex)
    
    while not Q.is_empty():
        u = Q.extract_minimum().value
        if S.search(u):
            continue
        else:
            S.insert(u, None)
            for v in range(vertex_count):
                _relax(u, v)
    path[source] = [source]
    return distance, path