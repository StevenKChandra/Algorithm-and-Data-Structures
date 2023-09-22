### Dijkstra's Algorithm to find a single source to other nodes 
def Dijkstra_Algorithm(graph, source):
    
    ### AUXILIARY FUNCTIONS ###
    ### initialize the distance and path placeholder
    def _initialize ():

        # call the required main function's variables
        nonlocal graph, source, vertex_count

        # create empty dictionary for distance and path
        d = {}
        p = {}

        # fill the dictionaries
        for vertex in range(vertex_count):
            
            # set the distance to all vertex to infinity
            d[vertex] = float("inf")
            
            # set the path to all vertex to an empty list
            p[vertex] = []
        
        # set the distance to the source as 0
        d[source] = 0

        # return the dictionaries
        return d, p
    
    ### create an adjacency matrix with where direct path weight from source to destination is AdjacencyMatrix[source][destination]
    def _Create_AdjacencyMatrix(graph):
        
        # call the required main function's variables
        nonlocal vertex_count

        # if the input is already an adjacency matrix
        if vertex_count == len(graph[0]) and (isinstance(graph[0][0], int) or isinstance(graph[0][0], float)):
           
           # return the adjacency matrix
           return graph
        
        # if the input is an adjacency list
        else:

            # create a placeholder for the adjacency matrix where all direct path's weight is infinite
            AdjacencyMatrix = [[float("inf") for i in range(vertex_count)] for y in range(vertex_count)]

            # iterate through the adjacency list
            for source in range (vertex_count):
                for destination, weight in graph[source]:

                    # replace the weight in adjacency matrix with the weight from the adjacency list
                    AdjacencyMatrix[source][destination] = weight
                
                # set the weight from and to the same vertex to 0
                AdjacencyMatrix [source][source] = 0
            
            # return the adjacency matrix
            return AdjacencyMatrix
    
    ### relaxation function to update the minimum distance and the path to a vertex
    def _relax(source, destination):

        # call the required main function's variables
        nonlocal distance, path, AdjacencyMatrix, Q

        # calculate the new path distance, total distance when using the intermediate vertex to the destination  
        new_distance = distance[source] +  AdjacencyMatrix[source][destination]

        # if the new path distance is lower than the old path distance
        if distance[destination] > new_distance:
            
            # update the minimum distance to the destination
            distance[destination] = new_distance

            # add the intermediate vertex to the path
            path[destination] = path[source] + [source]

            # insert the new distance to the destination to the priority queue
            Q.insert(new_distance, destination)
    
    ### MAIN CODE ###
    from Data_Structures import PriorityQueue, RedBlackTree

    # count the number of vertex
    vertex_count = len(graph)

    # create a placeholder for the distance and path to all destination
    distance, path = _initialize()

    # create an adjacency matrix of the graph
    AdjacencyMatrix = _Create_AdjacencyMatrix(graph)

    # create a priority queue
    Q = PriorityQueue()

    # fill the queue with distance as key and destination as value
    for vertex in range(vertex_count):
        Q.insert(distance[vertex], vertex)

    # create a red-black tree
    S = RedBlackTree()
    
    # keep going until the queue is empty
    while not Q.is_empty():

        # pull the vertex with minimum distance from the last vertex
        source = Q.extract_minimum().value

        # check if the vertex has been visited
        if S.search(source):

            # if yes, then the shortest path using this vertex as an intermediate vertex has been visited
            continue

        # if not use this as an intermediate vertex
        else:

            # save the intermediate vertex to the search tree
            S.insert(source, None)

            # try to go to all vertex from this intermediate vertex
            for destination in range(vertex_count):
                
                # relax the distance and path from the intermediate vertex to the destination
                _relax(source, destination)
    
    # set the path from a vertex to itself
    path[source] = [source]

    # return the distance and path from source to all other vertex
    return distance, path

### Floyd-Warshall Algorithm to find the shortest paths for all source to other nodes
def FloydWarshall_Algorithm(Graph):
    
    ### AUXILIARY FUNCTIONS ###
    ### create an adjacency matrix with where direct path weight from source to destination is AdjacencyMatrix[source][destination]
    def _Create_AdjacencyMatrix(graph):
        
        # call the required main function's variables
        nonlocal vertex_count

        # if the input is already an adjacency matrix
        if vertex_count == len(graph[0]) and (isinstance(graph[0][0], int) or isinstance(graph[0][0], float)):
           
           # return the adjacency matrix
           return graph
        
        # if the input is an adjacency list
        else:

            # create a placeholder for the adjacency matrix where all direct path's weight is infinite
            AdjacencyMatrix = [[float("inf") for i in range(vertex_count)] for y in range(vertex_count)]

            # iterate through the adjacency list
            for source in range (vertex_count):
                for destination, weight in graph[source]:

                    # replace the weight in adjacency matrix with the weight from the adjacency list
                    AdjacencyMatrix[source][destination] = weight
                
                # set the weight from and to the same vertex to 0
                AdjacencyMatrix [source][source] = 0
            
            # return the adjacency matrix
            return AdjacencyMatrix
    
    ### MAIN CODE ###
    # count the number of vertex
    vertex_count = len(Graph)

    # create an adjacency matrix from the input graph
    Graph = _Create_AdjacencyMatrix(Graph)

    # create a placeholder for the distance and the path
    D = [Graph]
    P = [[None if i == j or Graph[i][j] == float("inf") else i for j in range(vertex_count)] for i in range(vertex_count)]

    # iterate the adjacency list using k as our intermeidate vertex
    for k in range(vertex_count):

        # create a placeholder for the new distance and new path
        d = [[None for x in range (vertex_count)] for y in range(vertex_count)]
        p = [[None for x in range (vertex_count)] for y in range(vertex_count)]

        # iterate through source vertex i and destination vertex j
        for i in range(vertex_count):
            for j in range(vertex_count):

                # calculate the new distance from i to j using k as intermediate vertex
                new_distance = D[k][i][k] + D[k][k][j]

                # if the path from i to j using k as intermediate vertex is shorter
                if D[k][i][j] > new_distance:
                    
                    # use k as intermediate vertex
                    d[i][j] = new_distance
                    p[i][j] = P[k][k][j]
                
                # keep the current distance and path
                else:
                    d[i][j] = D[k][i][j]
                    p[i][j] = P[k][i][j]
        
        # update the placeholder
        D.append(d)
        P.append(p)
    
    # calculate the path from all source vertex to other vertexes
    path = []

    # iterate through all source vertexes
    for i in range(vertex_count):

        # create placeholder for current source vertex path
        p = []

        # iterate through all destination vertexes
        for j in range(vertex_count):

            # if source vertex and destination vertex are the same, set path as the said vertex
            if i == j:
                pp = [i]

            # if source vertex and destination vertex are the not same
            else:
                
                # k is the first intermediate vertex from the destination
                k = P[vertex_count][i][j]

                # if k is not none, then there is a path from the p
                if k != None:

                    # save the first intermediate vertex
                    pp = [k]
                    
                    # check if the intermediate vertex is the source vertex, if so then the path is complete
                    while k != i:

                        # if not, then change the intermediate vertex to the vertex before it
                        k = P[vertex_count][i][k]

                        # save the new intermediate vertex
                        pp.append(k)
                
                # if k is none, then there is no path from source 
                else:

                    # return empty path
                    pp = []
            
            # save the path from a destination vertex to the source vertex, but in reverse
            p.append(pp[::-1])
        
        # save all the path from one source vertex to other vertexes
        path.append(p)

    # return the distance matrix and path matrix
    return D[vertex_count], path