from typing import Self, List, Set, Hashable, Dict, Any

class Graph:
    """A directed graph data structure.

    A graph is a collection of vertices and edges.
    Edges in a graph might have values ascociated with them.
    """
    def __init__(self):
        """
        Initialize an empty graph.
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
            
        This method removes the specified vertex from the graph's
        vertices set, and deletes all edges (both inbound and outbound)
        associated with that vertex.

        Args:
            vertex: The vertex to be removed.

        Raises:
            ValueError: If the vertex is not in the graph.
        """
        if vertex not in self.vertices:
            raise ValueError("vertex not in graph")
        self.vertices.remove(vertex)

        if vertex in self.outbound_edges:
            for edge in self.outbound_edges[vertex]:
                self.inbound_edges[edge].remove(vertex)
            del self.inbound_edges[vertex]

        if vertex in self.inbound_edges:
            for edge in self.inbound_edges[vertex]:
                self.outbound_edges[edge].remove(vertex)
                
            del self.outbound_edges[vertex]

    def add_edge(self, source: Hashable, destination: Hashable) -> None:
        """Add a directed edge from source to destination.
            
        This method adds a directed edge from the source vertex to the
        destination vertex.

        Args:
            source: The source vertex.
            destination: The destination vertex.

        Raises:
            ValueError: If the source or destination vertex is not in
                the graph.
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

        This method removes the directed edge from the source vertex to
        the destination vertex in the graph.

        Args:
            source: The source vertex.
            destination: The destination vertex.

        Raises:
            ValueError: If there is no edge from source to destination
                in the graph.
        """
        if not self.is_adjacent(source, destination):
            raise ValueError("edge not in graph")
        
        del self.outbound_edges[source][destination]
        self.inbound_edges[destination].remove(source)

    def is_adjacent(self, source: Hashable, destination: Hashable) -> bool:
        """
        Check if there is a directed edge from source to destination.

        Args:
            source: The source vertex.
            destination: The destination vertex.

        Returns:
            bool: True if an edge from source to destination exists,
                False otherwise.
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

        This method sets the value associated with the edge from the
        source vertex to the destination vertex in the graph.

        Args:
            source: The source vertex.
            destination: The destination vertex.
            value: The value to set on the edge.

        Raises:
            ValueError: If there is no edge from source to destination
                in the graph.
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

        This method returns the value associated with the edge from the
        source vertex to the destination vertex in the graph.

        Args:
            source: The source vertex.
            destination: The destination vertex.

        Returns:
            Any: The value associated with the edge.

        Raises:
            ValueError: If there is no edge from source to destination
                in the graph.
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
    """A Priority Queue data structure that stores key and value pair.

    Each node on the priority queue is ordered based on its key in a 
    binary heap. All nodes in a priority queue have lower key value
    than its children.
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

        Args:
            key: An integer or float representing the key of the
                key-value pair.
            value: A hashable object representing the value of the
                key-value pair.

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
    children) have 2^k nodes.
    """

    class BinomialTreeNode:
        """A node of binomial tree"""

        def __init__(self, key: int|float, value: Hashable) -> None:
            """
            Initializes a BinomialTreeNode with the given key and value.

            Args:
                key: The key of the node, which should be an integer
                    or a float.
                value: The value associated with the node, which must
                    be hashable.
            """
            self.key: int|float = key
            self.value: any = value
            self.parent: Self|None = None
            self.degree: int = 0
            self.child: Self|None = None
            self.sibling: Self|None = None
    
    def __init__(self) -> None:
        """
        Initializes an empty BinomialHeap.
        """
        self._value_pointer: Dict[Hashable, BinomialHeap.BinomialTreeNode] = dict()
        self._head: BinomialHeap.BinomialTreeNode = None
        self._len: int = 0

    def is_empty(self) -> bool:
        """
        Check if the Binomial Heap is empty.

        Returns:
            bool: True if the heap is empty, False otherwise.
        """
        return len(self) == 0
    
    def minimum(self):
        """
        Finds and returns the value associated with the minimum key in
        the binomial heap.

        If the binomial heap is empty, an IndexError is raised.

        Returns:
            The value associated with the minimum key.

        Raises:
            IndexError: If the binomial heap is empty.
        """
        if (len(self) == 0):
            IndexError("Binomial Heap is empty")
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
        """
        Inserts a new key-value pair into the binomial heap.

        Args:
            key (int|float): The key for the new node, which must be an integer or float.
            value (Hashable): The value associated with the new node, which must be hashable.

        Raises:
            TypeError: If the key is not an integer or float.
            ValueError: If the value already exists in the heap.
        """
        if type(key) not in [int, float]:
            raise TypeError("key must be an integer or float")
        if key in self._value_pointer:
            raise ValueError("value already exists in the heap")
        
        node = self.BinomialTreeNode(key, value)
                
        heap = BinomialHeap()
        heap._value_pointer[value] = node
        heap._head = node
        heap._len = 1

        heap = self + heap

        self._head = heap._head
        self._len = heap._len
        self._value_pointer = heap._value_pointer
        
    def extract_min(self):
        """
        Extracts the node with the minimum key from the binomial
        heap and returns its value.

        The function traverses the heap to find the node with the
        minimum key, removes it, and restructures the heap to
        maintain the binomial heap properties.

        Raises:
            IndexError: If the binomial heap is empty.
        """
        if len(self) == 0:
            raise IndexError("Binomial Heap is empty")

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
    
    def decrease_key(self, value, new_key):
        """
        Decreases the key of the node associated with the given value in
        the binomial heap.

        Args:
            value (Hashable): The value associated with the node whose
                key is to be decreased.
            new_key (int|float): The new key to be associated with the
                node.

        Raises:
            ValueError: If the value does not exist in the heap, or if
                the new key is greater than the current key.
        """
        if value not in self._value_pointer:
            raise ValueError("value does not exist in the heap")
        
        if new_key >= self._value_pointer[value].key:
            raise ValueError("new key is greater than the current key")
        
        node = self._value_pointer[value]
        parent = node.parent

        node.key = new_key

        while node.parent != None and node.key < parent.key:
            node.key, parent.key = parent.key, node.key
            node.value, parent.value = parent.value, node.value
            self._value_pointer[node.value] = node
            self._value_pointer[parent.value] = parent
            node = parent
            parent = parent.parent

    def delete(self, value):
        """
        Deletes the node associated with the given value from the
        binomial heap.

        Args:
            value (Hashable): The value associated with the node to be
                deleted.

        Raises:
            ValueError: If the value does not exist in the heap.
        """
        self.decrease_key(value, float('-inf'))
        self.extract_min()

    def _binomial_heap_merge(self, other):
        """
        Merges two binomial heaps together into a single binomial heap.

        Args:
            other (BinomialHeap): The other heap to be merged.

        Returns:
            BinomialHeap: The merged heap.
        """
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
        self._value_pointer = self._value_pointer | other._value_pointer
        self._len += other._len

        return self
    
    def __add__(self, other):
        if other is not BinomialHeap:
            raise TypeError(f"unsupported operand type(s) for +: 'BinomialHeap' and '{type(other)}'.")
        if not self._value_pointer.keys().isdisjoint(other._value_pointer.keys()):
            raise ValueError("duplicate values in the heap")
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

    def _binomial_link(self, x, y):
        x.parent = y
        x.sibling = y.child
        y.child = x
        y.degree += 1

    def __len__(self) -> int:
        return self._len

class FibonacciHeap:
    class FibonacciHeapNode:
        def __init__(self, key: int|float, value: Hashable) -> None:
            if type(key) not in [int, float]:
                raise TypeError("key must be an integer or float")
            if value.__eq__ is None or value.__hash__ is None:
                raise TypeError("value must be hashable")
            self.key = key
            self.value = value
            self.degree = 0
            self.mark = False
            self.parent = None
            self.left = self
            self.right = self
            self.child = None

        def __add__(self,
            other: "FibonacciHeap.FibonacciHeapNode" = None
            ) -> "FibonacciHeap.FibonacciHeapNode":
            if other is None:
                return self
            
            self_next = self.right
            other_next = other.right

            self.right = other
            other.left = self
            self_next.left = other_next
            other_next.right = self_next

            return self
        
        def __len__(self) -> int:
            pointer = self
            count = 1
            while pointer.right != self:
                pointer = pointer.right
                count += 1
            return count
        
        def remove(self) -> None:
            self.left.right = self.right
            self.right.left = self.left
            
            self.right = self
            self.left = self

        def link(self, other: "FibonacciHeap.FibonacciHeapNode"):
            other.remove()
            self.child = other + self.child
            other.parent = self
            self.degree += 1
            other.mark = False
        
    def __init__(self) -> None:
        """
        Initializes an empty FibonacciHeap.
        """
        
        self._min = None
        self._len = 0
        self._value_pointer = dict()
    
    def is_empty(self) -> bool:
        """
        Check if the Fibonacci Heap is empty.

        Returns:
            bool: True if the heap is empty, False otherwise.
        """
        
        return len(self) == 0

    def insert(self, key: int|float, value: Hashable) -> None:
        """
        Inserts a key and value pair to the FibonacciHeap.

        Args:
            key: An integer or float representing the key of the key
                value pair.
            value: A hashable object representing the value of the key
                value pair.

        Raises:
            TypeError: If the key is not an integer or float.
            ValueError: If the value is not hashable.
            ValueError: If the value is already in the heap.
            
        """
        node = self.FibonacciHeapNode(key, value)
        if value in self._value_pointer:
            raise ValueError("value already exists in the heap")
        if self._min == None:
            self._min = node
        else:
            self._min += node
            if node.key < self._min.key:
                self._min = node
        self._value_pointer[value] = node
        self._len += 1

    def minimum(self) -> Hashable:
        """
        Returns the value associated with the minimum key in the
        FibonacciHeap.

        Returns:
            The value associated with the minimum key.

        Raises:
            IndexError: If the FibonacciHeap is empty.
        """
        return self._min.value
    
    def extract_min(self) -> Hashable:
        """
        Returns the value associated with the minimum key in the
        FibonacciHeap and removes the said key value pair.

        Returns:
            The value associated with the minimum key.

        Raises:
            IndexError: If the FibonacciHeap is empty.
        """
        if self.is_empty():
            raise IndexError("Fibonacci Heap is empty")
        
        value = self._min.value

        if self._min.child != None:
            pointer = self._min.child
            while pointer != self._min.child:
                pointer.parent = None
            self._min += self._min.child
        
        if self._min.right == self._min:
            self._min = None
        else:
            temp = self._min.right
            self._min.remove()
            self._min = temp
            self._consolidate()
        self._len -= 1
        del self._value_pointer[value]
        return value
    
    def _consolidate(self):
        placeholder = dict()
        pointer = self._min
        for i in range(len(self._min)):
            next = pointer.right
            while pointer.degree in placeholder:
                if pointer.key > placeholder[pointer.degree].key:
                    temp = pointer
                    pointer = placeholder[pointer.degree]
                    placeholder[pointer.degree] = temp
                pointer.link(placeholder[pointer.degree])
                del placeholder[pointer.degree-1]
            placeholder[pointer.degree] = pointer
            pointer = next

        minimum = BinomialHeap.BinomialTreeNode(float("inf"), None)
        for node in placeholder.values():
            if node != None:
                if node.key < minimum.key:
                    minimum = node
        self._min = minimum

    def __add__(self, other):
        if type(other) is not FibonacciHeap:
            raise TypeError(f"unsupported operand type(s) for +: 'FibonacciHeap' and '{type(other)}'.")
        if not self._value_pointer.keys().isdisjoint(other._value_pointer.keys()):
            raise ValueError("duplicate values in the heap")
        if len(self) == 0:
            return other
        if len(other) == 0:
            return self
        self._min = self._min + other._min
        heap = FibonacciHeap()
        if self._min.key < other._min.key:
            heap._min = self._min
        else:
            heap._min = other._min
        heap._len = self._len + other._len
        heap._value_pointer = self._value_pointer | other._value_pointer
        return heap

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
