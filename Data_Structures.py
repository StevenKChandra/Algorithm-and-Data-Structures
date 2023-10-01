class PriorityQueue:

    ### ON START ###
    def __init__(self):

        # set container as empty array and its length to 0
        self.container = []
        self.len = 0

    ### Define a nested class, the node of a priority queue
    class PriorityQueue_Node:
        
        ### takes an argument of key value pair
        def __init__(self, key, value):

            # set the key and value attribute
            self.key = key
            self.value = value

    ### MAIN FUNCTIONS ###

    ### function to insert an node to the Priority Queue
    def insert(self, key, value):
        
        key = str(key)

        # add the node at the end of the array
        self.container.append(self.PriorityQueue_Node(key, value))

        # add 1 the array length 
        self.len += 1

        # set current index as the array length
        index = self.len

        # find the parent's index of the current node's index
        parent = self._parent(index)

        # check if the current node key is smaller than its parrents key and the current node is not the root
        while index > 1 and self.container[index-1].key < self.container[parent-1].key:
            
            # swap the current node to its parent
            self.container[index-1], self.container[parent-1] = self.container[parent-1], self.container[index-1]

            # set the current node's index as its parrent's index and parent's index as current node's grandparent's index
            index, parent = parent, self._parent(parent)

    ### function to remove and return the node with minimum key
    def extract_minimum(self):
        
        # check if the Priority Queue is empty
        if not len(self.container):
            print("Queue is empty")

        else:

            # set the minimum node as first node
            min = self.container[0]
            
            # swap the first node with the last node
            self.container[0] = self.container[-1]

            # delete the last node and substract 1 from the array length
            self.container = self.container[:-1]
            self.len -= 1

            # perform heapify to the first node
            self._heapify(1)

            # return the minimum node
            return min
    
    ### function to return the node with minimum key
    def minimum(self):

        # check if the Priority Queue is empty
        if not len(self.container):
            print("Queue is empty")

        else:

            # return the first node
            return self.container[0]

    ### function to reduce the key of node i
    def decrease_key(self, index, key):
        
        # if the new key is lower than the old key
        if self.container[index-1].key > key:
            
            # replace the key
            self.container[index-1].key = key
            
            # perform heapify
            self._heapify(index)

    ### function to check if the Queue is emtpy
    def is_empty(self):
        if self.len:
            return False
        else:
            return True
        
    ### AUXILIARY FUNCTIONS ###

    ### fuction to "bubble" a node down if it is larger than one of its children
    def _heapify(self, index):

        # set the smallest node index to current index
        smallest = index

        # find the node left child and right child index
        left = self._left(index)
        right = self._right(index)

        # if current node key is larger than left child key:
        if left <= self.len:
            if self.container[index-1].key > self.container[left-1].key:

                # set smallest index to the left child
                smallest = left

        # if current node key is larger than right child key:
        if right <= self.len:
            if self.container[index-1].key > self.container[right-1].key:

                # set smallest index to the right child
                smallest = right
        
        # if the current node is  is larger than one of its children
        if smallest != index:

            # swap the node with the said children
            self.container[index-1], self.container[smallest-1] = self.container[smallest-1], self.container[index-1]
            
            # perform heapify recursively to the children 
            self._heapify(smallest)
    
    # function to return the parent's index of an index
    def _parent(self, index):
        return index // 2
    
    # function to return the left child's index of an index
    def _left(self, index):
        return index * 2
    
    # function to return the right child's index of an index
    def _right(self, index):
        return index * 2 + 1

class RedBlackTree:

    ### ON START ###
    def __init__(self):

        # set the tree root as a node
        self.root = self.RedBlackTree_Node(self, None)
    
    ### DEFINE A NESTED CLASS, THE RED-BLACK TREE NODE ###
    # Note that all the important functions will be written in this class
    class RedBlackTree_Node:

        ### set default node attributes as a leaf
        def __init__(self, tree, parent):
            
            # all leaf are black
            self.black = True

            # set the pointer to the tree and the node's parent
            self.tree = tree
            self.parent = parent

            # set all other values aas none
            self.key = None
            self.value = None
            self.left = None
            self.right = None
            
        ### MAIN FUNCTIONS ###

        ### function to insert a key-value pair
        def insert(self, key, value):

            # check if current node is not empty and have different key compared to the input key
            while self.key != None and self.key != key:

                # if the current node key is larger than the input key
                if self.key > key:

                    # set current node to the left
                    self = self.left
                
                # if the current node is larger than the input key
                else:

                    #set current node to the right
                    self = self.right
            
            # if current node key have different 
            if self.key != key:
                
                # set the color to red
                self.black = False

                # set the node key and value
                self.key = key
                self.value = value

                # create left and right children with empty key (leaves)
                self.left = self.tree.RedBlackTree_Node(self.tree, self)
                self.right = self.tree.RedBlackTree_Node(self.tree, self)

                # perform balancing function to preserve the red-black property
                self._insert_balance()
            
            # if the key is already exist in the tree
            else:

                # overwrite the value or not
                if input("key already exist, overwrite the value? (y/n)") == "y":
                    self.value = value

        ### function to find a node given the key
        def search(self, key):

            # check if the current node key is different from the target key and not empty
            while self.key != key and self.key != None:

                # if current node key is larger than the target key
                if self.key > key:
                    
                    # go to the left child
                    self = self.left
                
                # if current node key is smaller than the target key
                else:

                    # go to the right child
                    self = self.right
            
            # if the key is not empty, then the target key is in the tree
            if self.key != None:

                # return the node
                return self
            
            # else, the target key is not in the the tree
            else:
                # print("key not found")
                return None
            
        ### function to delete node with given the key
        def delete(self, key):

            # search the node to be deleted
            self = self.search(key)
            
            # if the search returns a node, delete it
            if self:
                
                # check if the node have less than two child
                if not self.left.value or not self.right.value:
                    
                    # if yes, we set the pointer to itself
                    pointer = self
                
                # if node have two child
                else:

                    # set the pointer to the node successor
                    pointer = self._successor()
                
                # if we are using a successor node, then it should have no left child
                if pointer.left.value:

                    # set a placeholder to hold the node left child
                    child = pointer.left
                
                # if we are using a successor node have right child
                else:

                    # set a placeholder to hold the pointer node right child
                    child = pointer.right
                
                # link the pointer child to the pointer's parent
                child.parent = pointer.parent

                # if the node is the root node
                if not pointer.parent:

                    # set the child node as the root
                    self.tree.root = child
                
                # if the node is not the root node
                else:

                    # if the node is a left child
                    if pointer == pointer.parent.left:

                        # link the node's parent to the node's child
                        pointer.parent.left = child

                    # if the node is a right child
                    else:

                        # link the node's parent to the node's child
                        pointer.parent.right = child
                
                # if we are using a successor node
                if pointer is not self:
                    
                    # replace the current node key and values with successor node
                    self.key = pointer.key
                    self.value = pointer.value
                
                # if the removed node is black, then the current pointer is considered to be "double black"
                # to preserve the red-black property
                if pointer.black:

                    # perform balancing function "push" the extra black to a red node and preserve the red-black property
                    child._delete_balance()

        ### do in order traversal using morris method
        def morris_inorder(self):

            # check if the node is not a leaf
            while self.key is not None:

                # if node does not have a left child
                if self.left.key is None:

                    # if not, print the key and set pointer on the right child
                    print (self.key, end = " ")
                    self = self.right
                
                # if node has a left child
                else :

                    # set pointer to the maximum of the left child
                    child = self.left
                    while child.right.key is not None and child.right != self:
                        child = child.right
                    
                    # if the maximum node does not have a right child (first time iterated)
                    if child.right.key is None:

                        # link the right child of the maximum node to the pointer
                        child.right = self
                        self = self.left

                    # the maximum node is already linked to the pointer (second time iterated)
                    else:

                        # fix the maximum node right child link
                        child.right = self.tree.RedBlackTree_Node(self.tree, child)
                        
                        # print the key and set pointer to tthe right child
                        print (self.key, end = " ")
                        self = self.right

        ### AUXILIARY FUNCTIONS ###

        ### function for preserving the red-black tree properties after inserting an element
        def _insert_balance(self):
            
            # check if node is the root
            while self.parent is not None and not self.parent.black:
                
                #check if the parent is a left child
                if self.parent == self.parent.parent.left:

                    # pointer for the node's "uncle"
                    pointer = self.parent.parent.right

                    # case 1: the uncle is red
                    if not pointer.black:

                        # swap the color of the parent and uncle to black and the grandparent to red
                        pointer.black = True
                        self.parent.black = True
                        self.parent.parent.black = False

                        # start balancing again from the grandparent
                        self = self.parent.parent
                    
                    
                    else:
                        # case 2: the node is a right child
                        if self == self.parent.right:

                            # do a left rotation to change the current case into a case 3
                            self.parent._rotate_left()
                            self = self.left

                        # case 3: the node is a left child
                        # swap the color of the parent and grandparent
                        self.parent.parent.black = False
                        self.parent.black = True

                        # do a right rotation on the grandparent
                        self.parent.parent._rotate_right()

                # if the parent is a right child
                # the code below is similar as the previous code, with "left" and "right" swapped
                else:

                    # pointer for the node's "uncle"
                    pointer = self.parent.parent.left

                    # case 4: the uncle is red
                    if not pointer.black:

                        # swap the color of the parent and uncle to black and the grandparent to red
                        pointer.black = True
                        self.parent.black = True
                        self.parent.parent.black = False

                        # start balancing again from the grandparent
                        self = self.parent.parent
                    
                    else:
                        # case 5: the node is a left child
                        if self == self.parent.left:

                            # do a right rotation to change the current case into a case 6
                            self.parent._rotate_right()
                            self = self.right

                        # case 6: the node is a right child
                        # swap the color of the parent and grandparent
                        self.parent.parent.black = False
                        self.parent.black = True

                        # do a left rotation on the grandparent
                        self.parent.parent._rotate_left()
            
            #check if current node is root
            if self.parent is None:

                # change color to black
                self.black = True
        
        ### function for preserving the red-black tree properties after deleting an element
        def _delete_balance(self):

            # continue the loop if the node is on a non-root black node
            while self.parent and self.black:
                
                # if node is a left child
                if self is self.parent.left:
                    
                    # set a pointer to the new sibling
                    sibling = self.parent.right

                    # case 1: the sibling is red
                    if not sibling.black:

                        # do left rotation on the parent node, swap the color of sibling and parent
                        sibling.black = True
                        self.parent.black = False
                        self.parent._rotate_left()
                        
                        # set the pointer to the new sibling
                        sibling = self.parent.right

                    # by performing case 1, now the sibling is also black
                    # case 2: both child of the sibling is black
                    if sibling.left.black and sibling.right.black:
                        
                        # push the extra black up to the parent
                        # do this by coloring the sibling node to red
                        # and setting the current node to the parent
                        sibling.black = False
                        self = self.parent
                    
                    
                    else:
                        # case 3: the left child of the sibling is red
                        if sibling.right.black:

                            # set the swap the color of the sibling and its left child
                            sibling.black = False
                            sibling.left.black = True

                            # do right rotation on the sibling
                            sibling._rotate_right()

                            # set the pointer to the new sibling
                            sibling = self.parent.right
                        
                        # case 4: the right child of the sibling is red

                        # change swap the color of the sibling and parent
                        sibling.black = self.parent.black
                        self.parent.black = True

                        # set the sibling's right child to black
                        sibling.right.black = True

                        # do left rotation on the parent node
                        self.parent._rotate_left()
                        
                        # go to the root node after case 4
                        self = self.tree.root

                # if the current node is a right child
                # the code below is symmetrical to the code before
                else:

                    sibling = self.parent.left
                    
                    if not sibling.black:

                        sibling.black = True
                        self.parent.black = False
                        self.parent._rotate_right()

                        sibling = self.parent.left
                    
                    if sibling.left.black and sibling.right.black:
                        sibling.black = False
                        self = self.parent
                    
                    else:
                        if sibling.left.black:
                            sibling.black = False
                            sibling.right.black = True
                            sibling._rotate_left()
                            sibling = self.parent.left
                        
                        sibling.black = self.parent.black
                        self.parent.black = True
                        sibling.left.black = True
                        self.parent._rotate_right()
                        
                        self = self.tree.root

            # color the current node to black, since it is either a red node or the root node
            self.black = True          

        ### function to find a node predecessor
        def _predecessor(self):

            # check if the node has a left child
            if self.left.key:

                # in that case the predecessor will be the maximum of the left child
                while self.right.key:
                    self = self.right
                return self

            # if not, find the closest ancestor whose right child is also an ancestor of the node
            while self.parent and self == self.parent.left:
                self = self.parent
            return self

        ### function to find a node successor
        def _successor(self):

            # check if the node has a right child
            if self.right.key:

                # in that case the predecessor will be the minimum of the right child
                while self.left.key:
                    self = self.left
                return self
            
            # if not, find the closest ancestor whose left child is also an ancestor of the node
            while self.parent and self == self.parent.right:
                self = self.parent
            return self
        
        ### function to perform tree rotations
        def _rotate_left(self):

            # define the pointers

            parent = self.parent
            child = self.right
            grandchild = child.left

            # check if node is not the root
            if parent:

                #check if node is a left child
                if self == parent.left:

                    # do bunch of swapping
                    (parent.left, child.parent, child.left, self.parent, self.right, grandchild.parent) = (child, parent, self, child, grandchild, self)
                
                #check if node is a right child
                else:

                    # do bunch of swapping
                    (parent.right, child.parent, child.left, self.parent, self.right, grandchild.parent) = (child, parent, self, child, grandchild, self)

            # check if node is the root
            else:

                # do bunch of swapping
                (self.tree.root, child.parent, child.left, self.parent, self.right, grandchild.parent) = (child, None, self, child, grandchild, self)

        def _rotate_right(self):

            # define the pointers

            parent = self.parent
            child = self.left
            grandchild = child.right

            # check if node is not the root
            if parent:

                #check if node is a left child
                if self == parent.left:

                    # do bunch of swapping
                    (parent.left, child.parent, child.right, self.parent, self.left, grandchild.parent) = (child, parent, self, child, grandchild, self)
                
                #check if node is a right child
                else:

                    # do bunch of swapping
                    (parent.right, child.parent, child.right, self.parent, self.left, grandchild.parent) = (child, parent, self, child, grandchild, self)

            # check if node is the root
            else:
                
                # do bunch of swapping
                (self.tree.root, child.parent, child.right, self.parent, self.left, grandchild.parent) = (child, None, self, child, grandchild, self)

        ### debugging function to test the red-black tree properties
        def check_redblack_property(self):
            ordered = []
            while self.key is not None:
                if self.left.key is None:
                    ordered.append(self.key)
                    if not self.black:
                        if not self.right.black and not self.left.black:
                            print("red node with red child(ren) detected")
                    self = self.right
                else :
                    child = self.left
                    while child.right.key is not None and child.right != self:
                        child = child.right
                    
                    if child.right.key is None:
                        child.right = self
                        self = self.left
                    else:
                        child.right = self.tree.RedBlackTree_Node(self.tree, child)
                        ordered.append(self.key)
                        if not self.black:
                            if not self.right.black and not self.left.black:
                                print("red node with red child(ren) detected")
                        self = self.right
            for i in range(len(ordered)-1):
                if ordered[i] > ordered[i+1]:
                    print("wrong order detected")

    ### FUNCTIONS TO CALL THE ROOT'S FUNCTIONS ###
    
    def insert(self, key, value):
        self.root.insert(key, value)

    def search(self, key):
        return self.root.search(key)

    def delete(self, key):
        self.root.delete(key)
    
    def morris_inorder(self):
        self.root.morris_inorder()

    def check_redblack_property(self):
        self.root.check_redblack_property()

class Graph():

    ### initialization function, expects an integer which is the number of vertices
    def __init__(self, NumberOfVertices):

        # set all the edge weights in adjacency matrix to infinite (infinity weight here means the edged does not exist) or zero for all vertex to itself 
        self.__AdjacencyMatrix = [[float("inf") if i!=j else 0.0 for i in range(NumberOfVertices)] for j in range(NumberOfVertices)]

        # create a list that maps vertex index (int) to its name (int). set the default values (its index)
        self.__VertexName = [str(i) for i in range(NumberOfVertices)]

        # save the number of vertices
        self.__NumberOfVertices = NumberOfVertices

    ### the two function below returns and sets the vertex name given the vertex index
    def GetNodeName(self, VertexIndex):
        return self.__VertexName[VertexIndex]
    
    def SetNodeName(self, VertexIndex, VertexName):
        self.__VertexName[VertexIndex] = VertexName

    ### the two function below returns and sets the vertex weight given the source vertex and the destination vertex
    def GetEdgeWeight(self, source, destination):
        return self.__AdjacencyMatrix[source][destination]
    def SetEdgeWeight(self, source, destination, weight):
        self.__AdjacencyMatrix[source][destination] = weight
    
    ### the two function below returns the number of vertices and edges
    def VerticesCount(self):
        return self.__NumberOfVertices
    def EdgesCount(self):
        count = 0
        for source in range(self.__NumberOfVertices):
            for destination in range(source+1, self.__NumberOfVertices):
                if self.__AdjacencyMatrix[source][destination] != float("inf") and self.__AdjacencyMatrix[source][destination] != float(0.0):
                    count += 1
        return count
    
    ### function to check if the given source vertex and destination vertex is adjacent
    def IsAdjacent(self, source, destination):
        return self.__AdjacencyMatrix[source][destination] != 0.0 and self.__AdjacencyMatrix[source][destination] != float("inf")

    ### function that returns the neighbor indices of a given source node
    def FindNeighbors(self, source):
        neighbors = []

        # iterate through the adjacency matrix
        for neighbor in self.__AdjacencyMatrix[source]:

            # if the neighbors
            if neighbor != float("inf") and neighbor!=0.0:
                neighbors.append(neighbor)
        return neighbors
    
    ### function to generate random edges in a graph, the function assumes the current graph does not have any edges
    def GenerateRandomEdges(self, GraphDensity, MinDistance, MaxDistance, IsDirectedGraph = False):

        # density (float) is the ratio of existing edges (not including edges from vertex to itself) and (number of vertices - 1) squared
        # MinDistace and MaxDistance (floats) are the range of the distance generated
        # IsDirected is the number of
        from random import random, uniform

        # iterate through the adjacency matrix
        for source in range(self.__NumberOfVertices):
            for destination in range(source+1, self.__NumberOfVertices):

                # generate random float [0,1] if smaller or equal to the density, generate an edge
                if random() <= GraphDensity:

                    # set the distance between min and max distance
                    self.__AdjacencyMatrix[source][destination] = uniform(MinDistance, MaxDistance)
                    
                    # if the graph is directed
                    if IsDirectedGraph:

                        # repeat the edge generation process for the mirroring position in the matrix
                        if random() >= GraphDensity:
                            self.__AdjacencyMatrix[destination][source] = uniform(MinDistance, MaxDistance)
                    
                    # if the graph is not directed
                    else:

                        # set the same distance for the mirroring position in the matrix
                        self.__AdjacencyMatrix[destination][source] = self.__AdjacencyMatrix[source][destination]

