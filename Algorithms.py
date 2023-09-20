def Djikstra_Algorithm(graph, source):
    
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

def FloydWarshall_Algorithm(Graph):
    n = len(Graph)
    D = [Graph]
    P = []
    for i in range(n):
        p = []
        for j in range(n):
            if i == j or Graph[i][j] == float("inf"):
                p.append(None)
            else:
                p.append(i)
        P.append(p)
    P = [P]

    for k in range(n):
        d = [[None for x in range (n)] for y in range(n)]
        p = [[None for x in range (n)] for y in range(n)]
        for i in range(n):
            for j in range(n):
                new_distance = D[k][i][k] + D[k][k][j]
                if D[k][i][j] > new_distance:
                    d[i][j] = new_distance
                    p[i][j] = P[k][k][j]
                else:
                    d[i][j] = D[k][i][j]
                    p[i][j] = P[k][i][j]
        D.append(d)
        P.append(p)
    path = []
    for i in range(n):
        p = []
        for j in range(n):
            if i == j:
                pp = [i]
            else:
                k = P[n][i][j]
                if k != None:
                    pp = [k]
                    while k != i:
                        k = P[n][i][k]
                        pp.append(k)
                else:
                    pp = []
            p.append(pp[::-1])
        path.append(p)

    return D[n], path