from unittest import TestCase

from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class TestGraphAlgo(TestCase):
    g1: GraphAlgo = GraphAlgo()

    def test_load_json(self):
        file_path = '../data/A0.json'
        ga = GraphAlgo()
        self.assertTrue(ga.load_from_json(file_path))
        g = ga.get_graph()
        self.assertEqual(g.__str__(), ga.__str__())

    def test_save_json(self):
        file_path1 = '../data/A0.json_new'
        file_path = '../data/A0.json'
        ga = GraphAlgo()
        self.assertTrue(ga.load_from_json(file_path))
        self.assertTrue(ga.save_to_json(file_path1))
        g = ga.get_graph()
        self.assertEqual(g.__str__(), ga.__str__())

    def test_is_connected(self):
        file = "../data/A0.json"
        graph_algo = GraphAlgo()
        graph_algo.load_from_json(file)
        self.assertTrue(graph_algo.is_connected())
        file = "../data/T0.json"
        graph_algo.load_from_json(file)
        self.assertFalse(graph_algo.is_connected())

    def test_shortest_path(self):
        g = self.simple_graph()
        ga = GraphAlgo(g)
        self.assertTupleEqual((3.0, [1, 2, 3, 7]), ga.shortest_path(1, 7))
        self.assertEqual((float('inf'), []), ga.shortest_path(1, 88))
        self.assertEqual((9.0, [3, 7, 8, 9]), ga.shortest_path(3, 9))

    def test_tsp(self):
        g = self.simple_graph()
        ga = GraphAlgo(g)
        self.assertTupleEqual(([1, 2, 8], 1.5), ga.TSP([1, 8]))
        self.assertEqual(([7, 8, 9, 1], 12.0), ga.TSP([7, 1]))
        ans = ga.TSP([7, 1, 4, 9])
        self.assertEqual(3, ans[0][1])
        self.g1.load_from_json("../data/G1.json")
        cities1 = [0]
        i = 0
        ans = self.g1.TSP(cities1)[0]
        while i < len(ans):
            self.assertEqual(cities1[i], ans[i])
            i += 1
        self.assertEqual(0, self.g1.TSP(cities1)[1])

        cities2 = []
        for n in self.g1.graph.nodes.values():
            cities2.append(n.key)
        self.assertEqual(22.63446693792369, self.g1.TSP(cities2)[1])



    def test_center_point(self):
        file = "../data/A0.json"
        graph_algo = GraphAlgo()
        b = graph_algo.load_from_json(file)
        print(b)
        self.assertTrue(graph_algo.load_from_json(file))
        self.assertEqual((7, 6.806805834715163), graph_algo.centerPoint())

        file = '../data/A1.json'
        graph_algo = GraphAlgo()
        self.assertTrue(graph_algo.load_from_json(file))
        self.assertEqual((8, 9.925289024973141), graph_algo.centerPoint())

        file = '../data/A2.json'
        graph_algo = GraphAlgo()
        self.assertTrue(graph_algo.load_from_json(file))
        self.assertEqual((0, 7.819910602212574), graph_algo.centerPoint())

        file = '../data/A3.json'
        graph_algo = GraphAlgo()
        self.assertTrue(graph_algo.load_from_json(file))
        self.assertEqual((2, 8.182236568942237), graph_algo.centerPoint())

        file = '../data/A4.json'
        graph_algo = GraphAlgo()
        self.assertTrue(graph_algo.load_from_json(file))
        self.assertEqual((6, 8.071366078651435), graph_algo.centerPoint())

        file = '../data/A5.json'
        graph_algo = GraphAlgo()
        self.assertTrue(graph_algo.load_from_json(file))
        self.assertEqual((40, 9.291743173960954), graph_algo.centerPoint())
        #
        # file = '../data/1000Nodes.json'
        # graph_algo = GraphAlgo()
        # self.assertTrue(graph_algo.load_from_json(file))
        # self.assertEqual((362, 1185.9594924690523), graph_algo.centerPoint())

    @staticmethod
    def simple_graph():
        """
        DiGraph: |V| = 10	|E| = 16
        {0: (0), 1: (1), 2: (2), 3: (3), 4: (4), 5: (5), 6: (6), 7: (7), 8: (8), 9: (9)}
        Edge Data:
        (1) -> {9: 0.5, 2: 0.5}
        (2) -> {8: 1.0, 3: 1.0}
        (3) -> {7: 1.5, 4: 1.5}
        (4) -> {6: 2.0, 5: 2.0}
        (5) -> {6: 2.5}
        (6) -> {4: 3.0, 7: 3.0}
        (7) -> {3: 3.5, 8: 3.5}
        (8) -> {2: 4.0, 9: 4.0}
        (9) -> {1: 4.5}
        https://user-images.githubusercontent.com/73063199/103218639-3a423580-4924-11eb-8316-f438c2846570.png      """
        g = DiGraph()
        for i in range(10):
            g.add_node(i)

        for i in range(10):
            g.add_edge(i, 10 - i, i * 0.5)
            g.add_edge(i, i + 1, i * 0.5)
        return g
