from typing import Self, List, Set, Hashable, Dict, Any

class Graph:
    def __init__(self):
        """
        Initialize an empty graph
        """
        self.vertices: Set[Hashable] = set()
        self.outbound_edges: Dict[Hashable, Dict[Hashable]] = dict()
        self.inbound_edges: Dict[Hashable, Set[Hashable]] = dict()

    def add_vertex(self, vertex: Hashable) -> None:
        """Add a vertex to the graph. The vertex name must be hashable
        and unique.

        Args:
            vertex: The vertex to add to the graph.

        Raises:
            TypeError: If the vertex name is not hashable.
            ValueError: If the vertex is already in the graph.
        """
        if vertex.__eq__ is None or vertex.__hash__ is None:
            raise TypeError("vertex name must be hashable")
        if vertex in self.vertices:
            raise ValueError("vertex already in graph")
        self.vertices.add(vertex)

    def remove_vertex(self, vertex: Hashable) -> None:
        """Remove a vertex and its associated edges from the graph.
            
        This method removes the specified vertex from the graph's vertices set,
        and deletes all edges (both inbound and outbound) associated with that vertex.

        Args:
            vertex: The vertex to be removed.

        Raises:
            ValueError: If the vertex is not in the graph.
        """
        if vertex not in self.vertices:
            raise ValueError("vertex not in graph")
        self.vertices.remove(vertex)

        for edge in self.outbound_edges[vertex]:
            self.inbound_edges[edge].remove(vertex)

        for edge in self.inbound_edges[vertex]:
            self.outbound_edges[edge].remove(vertex)

        if vertex in self.outbound_edges:
            del self.outbound_edges[vertex]

        if vertex in self.inbound_edges:
            del self.inbound_edges[vertex]

    def add_edge(self, source: Hashable, destination: Hashable) -> None:
        """Add a directed edge from source to destination.
            
        This method adds a directed edge from the source vertex to the destination vertex.

        Args:
            source: The source vertex.
            destination: The destination vertex.

        Raises:
            ValueError: If the source or destination vertex is not in the graph.
        """
        self._check_vertices(source, destination)
        
        if not source in self.outbound_edges:
            self.outbound_edges[source] = dict()
        self.outbound_edges[source][destination] = None

        if not destination in self.inbound_edges:
            self.inbound_edges[destination] = set()
        self.inbound_edges[destination].add(source)
    
    def remove_edge(self, source: Hashable, destination: Hashable) -> None:
        """
        Remove a directed edge from source to destination.

        This method removes the directed edge from the source vertex to the destination
        vertex in the graph.

        Args:
            source: The source vertex.
            destination: The destination vertex.

        Raises:
            ValueError: If there is no edge from source to destination in the graph.
        """
        if not self.is_adjacent(source, destination):
            raise ValueError("edge not in graph")
        
        del self.outbound_edges[source][destination]
        self.inbound_edges[destination].remove(source)

    def is_adjacent(self, source: Hashable, destination: Hashable) -> bool:
        """
        Check if there is a directed edge from source to destination.

        This method returns True if and only if there is a directed edge from the
        source vertex to the destination vertex in the graph, and False otherwise.

        Args:
            source: The source vertex.
            destination: The destination vertex.

        Returns:
            bool: True if an edge from source to destination exists, False otherwise.
        """
        self._check_vertices(source, destination)
        if source not in self.outbound_edges:
            return False
        return destination in self.outbound_edges[source]
    
    def set_edge_value(self,
        source: Hashable,
        destination: Hashable,
        value: Any
        ) -> None:
        """
        Set the value of an edge from source to destination.

        This method sets the value associated with the edge from the source
        vertex to the destination vertex in the graph.

        Args:
            source: The source vertex.
            destination: The destination vertex.
            value: The value to set on the edge.

        Raises:
            ValueError: If there is no edge from source to destination in the graph.
        """
        if not self.is_adjacent(source, destination):
            raise ValueError("edge not in graph")
        self.outbound_edges[source][destination] = value

    def get_edge_value(self,
        source: Hashable,
        destination: Hashable,
        ) -> Any:
        """
        Get the value associated with an edge from source to destination.

        This method returns the value associated with the edge from the source
        vertex to the destination vertex in the graph.

        Args:
            source: The source vertex.
            destination: The destination vertex.

        Returns:
            Any: The value associated with the edge.

        Raises:
            ValueError: If there is no edge from source to destination in the graph.
        """
       
        if not self.is_adjacent(source, destination):
            raise ValueError("edge not in graph")
        return self.outbound_edges[source][destination]

    def _check_vertices(self, source: Hashable, destination: Hashable) -> None:
        if source not in self.vertices:
            raise ValueError("source vertex not in graph")
        if destination not in self.vertices:
            raise ValueError("destination vertex not in graph")
        if source == destination:
            raise ValueError("source and destination cannot be the same")

class PriorityQueue:
    """
    A Priority Queue data structure that stores key and value pair.
    Each node on the priority queue is ordered based on its key.

    Methods:
        insert(key, value): inserts a key and value pair to the
            priority queue
        extract_minimum(): returns the node with minimum key and removes
            it from the priority queue
        minimum(): returns the node with minimum key
        is_empty(): returns True if and only if the priority queue is
            empty
    """

    ### Abstraction Function:
    #   the key value pairs in the priority queue is stored the
    #   self._container list. The root of the priority queue is the
    #   first element in the list. Each element's parents are
    #   elements with index i // 2, and children are elements
    #   with index 2i (left child) and 2i + 1 (right child) using 1
    #   based indexing.
    #   
    #   self._value_to_index maps each value to its index in the
    #   self._container list to help with decrease_key() method,

    class PriorityQueueNode:
        def __init__(self, key: int|float, value: Hashable) -> None:
            if type(key) not in [int, float]:
                raise TypeError("key must be an integer or float")
            self.key: int|float = key
            if value.__eq__ is None or value.__hash__ is None:
                raise TypeError("value must be hashable")
            self.value = value

    def __init__(self) -> None:
        """
        Initializes an empty Priority Queue.
        """
        self._container: List[PriorityQueue.PriorityQueueNode] = []
        self._value_to_index: dict[Any, int] = {}

    def insert(self, key: int|float, value) -> None:
        """
        Inserts a key and value pair to the priority queue.

        The key value pair is appended to the end of the priority queue and
        then heapify up is called to maintain the priority queue property.

        Args:
            key: An integer or float representing the key of the key value pair.
            value: A hashable object representing the value of the key value pair.

        Raises:
            ValueError: If the value is already in the priority queue.
        """

        if value in self._value_to_index:
            raise ValueError("value already in Priority Queue")
        self._container.append(self.PriorityQueueNode(key, value))
        index = len(self)
        self._value_to_index[value] = index
        self._heapify_up(index)

    def extract_minimum(self) -> Hashable:
        """Returns the value of key value pair with minimum key and
        removes the said key value pair.

        Returns:
        None if the Priority Queue is empty.
        the value of key value pair that has the lowest key otherwise.
        """
        if self.is_empty():
            raise IndexError("Priority Queue is empty")
        
        min = self._container[0]

        self._container[0] = self._container[-1]
        self._value_to_index[self._container[0]] = 0

        self._container = self._container[:-1]
        self._heapify_down(1)

        return min.value
    
    
    def minimum(self) -> Hashable:
        """Returns the value of key value pair that has the lowest key.

        Returns:
        None if the Priority Queue is empty.
        the value of key value pair that has the lowest key otherwise.
        """
        if self.is_empty():
            raise IndexError("Priority Queue is empty")
        
        return self._container[0].value

    """Reduce a key of a value"""
    def decrease_key(self, value, new_key: int|float)->None:
        index = self._value_to_index[value]

        if self._container[index-1].key < new_key:
            raise ValueError("new key is larger than current key")
        
        self._container[index-1].key = new_key
        self._heapify_up(index)

    def is_empty(self) -> bool:
        """Check if the Priority Queue is empty.

        Returns: 
        true if and only if the Priority Queue has no element
        """
        return len(self) == 0
        
    def __len__(self) -> int:
        """Returns the number of elements in the Priority Queue."""
        return len(self._container)
    
    def _heapify_down(self, index: int) -> None:
        """Pefroms "bubble down" on the node at index, if it is larger
        than one of its children."""
        left = self._left(index)
        right = self._right(index)

        smallest = index
        if left <= len(self):
            if self._container[smallest-1].key > self._container[left-1].key:
                smallest = left
        if right <= len(self):
            if self._container[smallest-1].key > self._container[right-1].key:
                smallest = right
        
        if smallest != index:
            placeholder = self._container[index-1]
            self._container[index-1] = self._container[smallest-1]
            self._container[smallest-1] = placeholder
            self._update_value_to_index(index)
            self._update_value_to_index(smallest)
            self._heapify_down(smallest)

    def _heapify_up(self, index:int) -> None:
        """Pefroms "bubble up" on the node at index, if it is smaller
        than its parent."""
        if index == 1:
            return
        parent_index = self._parent(index)
        if self._container[index-1].key < self._container[parent_index-1].key:
            placeholder = self._container[index-1]
            self._container[index-1] = self._container[parent_index-1]
            self._container[parent_index-1] = placeholder
            self._update_value_to_index(index)
            self._update_value_to_index(parent_index)
            self._heapify_up(parent_index)

    def _parent(self, index: int) -> int:
        "Returns the parent's index given an element's index"
        return index // 2
    
    def _left(self, index: int) -> int:
        """"Returns the left child's index given an element's index"""
        return index * 2
    
    def _right(self, index: int) -> int:
        """Returns the right child's index given an element's index"""
        return index * 2 + 1
    
    def _update_value_to_index(self, index: int) -> None:
        """Updates the value to index mapping"""
        self._value_to_index[self._container[index-1].value] = index

class BinomialHeap:
    """Binomial Heap data structure.
    
    Binomial heap is a collection of binomial trees that is heap ordered
    (all node's key is smaller than its children's key)
    A binomial tree with degree k (k is the number of the root's node
    children) have 2^k nodes."""

    class BinomialTreeNode:
        """A node of binomial tree"""

        def __init__(self, key: int|float, value) -> None:
            """Initializes a node of binomial tree.

            Args:
            key: takes an integer or float as the key.
            value: any immutable data types.
            """
            self.key: int|float = key
            self.value: any = value
            self.parent: Self|None = None
            self.degree: int = 0
            self.child: Self|None = None
            self.sibling: Self|None = None
    
    def __init__(self) -> None:
        self._head: BinomialHeap.BinomialTreeNode = None
        self._len: int = 0

    def is_empty(self) -> bool:
        return len(self) == 0
    
    def minimum(self):
        if (len(self) == 0):
            print("Binomial heap is empty.")
            return
        val = None
        pointer = self._head
        min_key = float("inf")
        while (pointer != None):
            if min_key > val.key:
                min_key = val.key
                val = pointer.val
        return val
    
    def insert(self, key: int|float, value) -> None:
        heap = BinomialHeap()
        head = self.BinomialTreeNode(key, value)
        heap._head = head
        heap._len = 1
        heap = self + heap
        self._head = heap._head
        self._len = heap._len

    def _binomial_heap_merge(self, other):
        if self.is_empty() or other.is_empty():
            return self if other.is_empty() else other
        
        new_head = self.BinomialTreeNode(0, None)
        pointer = new_head

        while (self._head != None and other._head != None):
            if self._head.degree < other._head.degree:
                pointer.sibling = self._head
                self._head = self._head.sibling
                pointer = pointer.sibling
            else:
                pointer.sibling = other._head
                other._head = other._head.sibling
                pointer = pointer.sibling

        pointer.sibling = other._head if self._head == None else self._head
        self._head = new_head.sibling
        self._len += other._len

        return self
    
    def __add__(self, other):
        heap = self._binomial_heap_merge(other)
        if (heap._head == None):
            return heap
        prev_x = None
        x = heap._head
        next_x = x.sibling
        while (next_x != None):
            if (x.degree != next_x.degree or 
                (next_x.sibling != None and 
                 next_x.sibling.degree == x.degree)):
                prev_x = x
                x = next_x
            elif (x.key <= next_x.key):
                x.sibling = next_x.sibling
                self._binomial_link(next_x, x)
            else:
                if prev_x == None:
                    heap._head = next_x
                else:
                    prev_x.sibling = next_x
                self._binomial_link(x, next_x)
                x = next_x
            next_x = x.sibling
        return heap
    
    def find_min(self):
        if len(self) == 0:
            print("heap is empty")

        minimum = float('inf')
        minimum_node = None

        x = self._head
        while x != None:
            if x.key < minimum:
                minimum = x.key
                minimum_node = x
            x = x.sibling

        return minimum_node.value
    
    def extract_min(self):
        if len(self) == 0:
            print("heap is empty")

        minimum = float('inf')
        minimum_node = None

        x = self._head
        while x != None:
            if x.key < minimum:
                minimum = x.key
                minimum_node = x
            x = x.sibling

        if minimum_node == self._head:
            self._head = minimum_node.sibling
        else:
            while x.sibling != minimum_node:
                x = x.sibling
            x.sibling = x.sibling.sibling

        self._len -= 2 ** minimum_node.degree

        if minimum_node.child == None:
            return

        new_heap = BinomialHeap()
        previous = None
        current = minimum_node.child
        next = current.sibling
        while next != None:
            current.parent = None
            current.sibling = previous
            new_heap._len += 2 ** current.degree
            previous = current
            current = next
            next = next.sibling
        current.parent = None
        current.sibling = previous
        new_heap._len += 2 ** current.degree
        new_heap._head = current

        new_heap = self + new_heap
        self._head = new_heap._head
        self._len = new_heap._len

    def _binomial_link(self, x, y):
        x.parent = y
        x.sibling = y.child
        y.child = x
        y.degree += 1

    def __len__(self) -> int:
        return self._len
    
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
