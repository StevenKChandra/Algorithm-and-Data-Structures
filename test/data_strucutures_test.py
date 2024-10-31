import unittest
from data_structures import Graph, PriorityQueue

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

    def test_add_vertex(self):
        self.graph.add_vertex(1)
        self.assertIn(1, self.graph.vertices)
        self.graph.add_vertex(2)
        self.assertIn(2, self.graph.vertices)

    def test_remove_vertex(self):
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_vertex(3)
        self.graph.remove_vertex(2)
        self.assertNotIn(2, self.graph.vertices)
        self.assertIn(1, self.graph.vertices)
        self.assertIn(3, self.graph.vertices)

    def test_add_edge(self):
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_edge(1, 2)
        self.assertIn(2, self.graph.outbound_edges[1])
        self.assertIn(1, self.graph.inbound_edges[2])

    def test_remove_edge(self):
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_edge(1, 2)
        self.graph.remove_edge(1, 2)
        self.assertNotIn(2, self.graph.outbound_edges[1])
        self.assertNotIn(1, self.graph.inbound_edges[2])

    def test_is_adjacent(self):
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_edge(1, 2)
        self.assertTrue(self.graph.is_adjacent(1, 2))
        self.assertFalse(self.graph.is_adjacent(2, 1))
        self.assertFalse(self.graph.is_adjacent(1, 3))

class TestPriorityQueue(unittest.TestCase):
    def test_insert(self):
        pq = PriorityQueue()
        pq.insert(1, "high priority")
        pq.insert(2, "medium priority")
        pq.insert(3, "low priority")
        self.assertEqual(len(pq), 3)

    def test_extract_minimum(self):
        pq = PriorityQueue()
        pq.insert(1, "high priority")
        pq.insert(2, "medium priority")
        pq.insert(3, "low priority")
        self.assertEqual(pq.extract_minimum(), "high priority")
        self.assertEqual(len(pq), 2)

    def test_minimum(self):
        pq = PriorityQueue()
        pq.insert(1, "high priority")
        pq.insert(2, "medium priority")
        pq.insert(3, "low priority")
        self.assertEqual(pq.minimum(), "high priority")
        self.assertEqual(len(pq), 3)

    def test_is_empty(self):
        pq = PriorityQueue()
        self.assertTrue(pq.is_empty())
        pq.insert(1, "high priority")
        self.assertFalse(pq.is_empty())

    def test_decrease_key(self):
        pq = PriorityQueue()
        pq.insert(3, "low priority")
        pq.insert(2, "medium priority")
        pq.insert(1, "high priority")
        pq.decrease_key("low priority", 0)
        self.assertEqual(pq.minimum(), "low priority")

    def test_extract_minimum_empty_queue(self):
        pq = PriorityQueue()
        with self.assertRaises(IndexError):
            pq.extract_minimum()

    def test_minimum_empty_queue(self):
        pq = PriorityQueue()
        with self.assertRaises(IndexError):
            pq.minimum()

    def test_insert_duplicate_value(self):
        pq = PriorityQueue()
        pq.insert(1, "high priority")
        with self.assertRaises(ValueError):
            pq.insert(2, "high priority")

if __name__ == '__main__':
    unittest.main()