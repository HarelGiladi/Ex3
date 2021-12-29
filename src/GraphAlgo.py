import json
import sys
from random import randint
from typing import List

from matplotlib import pyplot as plt
from PriorityQ import PriorityQueue
# from queue import PriorityQueue
from src.DiGraph import DiGraph
from src.GLocation import GLocation
from src.Node import Node
from src.GraphAlgoInterface import GraphAlgoInterface
from src.GraphInterface import GraphInterface
import copy


# need to be change!!
def bfs(n: Node, graph: DiGraph) -> bool:
    q = []
    n.info = "black"
    count = 1
    q.append(n)
    while len(q) > 0:
        temp = q.pop(0)
        if graph.edges.get(temp.key) is not None:
            for e in graph.edges.get(temp.key).values():
                dest = graph.getnode(e.dst)
                if dest.info == "white":
                    dest.info = "black"
                    q.append(dest)
                    count += 1
    return count == graph.v_size()


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g: DiGraph = DiGraph()) -> None:
        self.graph = copy.deepcopy(g)

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        # with open(file_name, 'r') as f:
        #     data = json.load(f)
        # l_nodes = data["Nodes"]
        # l_edges = data["Edges"]
        # for dic_nodes in l_nodes:
        #     pos = dic_nodes["pos"].split(',')
        #     self.graph.add_node(dic_nodes['id'], (float(pos[0]), float(pos[1]), float(pos[2])))
        # for dic_edges in l_edges:
        #     self.graph.add_edge(dic_edges['src'], dic_edges['dest'], dic_edges['w'])
        # return True
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
                g = DiGraph()
                for i in data['Nodes']:
                    if 'pos' in i.keys():
                        str_lst = i['pos'].split(',')
                        pos = (float(str_lst[0]), float(str_lst[1]), 0.0)
                        g.add_node(i['id'], pos)
                    else:
                        pos = (randint(35185, 35215) / 1000, randint(32101, 32108) / 1000, 0.0)
                        g.add_node(i['id'], pos)
                for i in data['Edges']:
                    g.add_edge(i['src'], i['dest'], i['w'])
                self.graph = g

        except Exception as e:
            print(e)
            return False

        return True

    def save_to_json(self, file_name: str) -> bool:
        node = []
        edge = []
        for n in self.graph.nodes.values():
            node.append(n)
        for d in self.graph.edges:
            for j in self.graph.edges.get(d).values():
                edge.append(j)

        save = {"Edges": [], "Nodes": []}
        for i in node:
            if i.location is None:
                save["Nodes"].append({"id": i.key})
            else:
                s = str(i.location.x) + "," + str(i.location.y) + "," + str(i.location.z)
                save["Nodes"].append({"id": i.key, "pos": s})
        for j in edge:
            save["Edges"].append({"src": j.src, "dest": j.dst, "w": j.weight})
        try:
            with open(file_name, 'w') as file:
                json.dump(save, indent=2, fp=file)

        except Exception:
            return False
        return True

    def is_connected(self) -> bool:
        if self.graph.v_size() == 0:
            return True
        n = self.graph.getnode(0)
        bfs(n, self.graph)
        for v1 in self.graph.nodes.values():
            if v1.info == "white":
                return False
        self.origin_all()
        c = self.converse()
        bfs(n, c)
        for v2 in c.nodes.values():
            if v2.info == "white":
                return False
        return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        ans_list = []
        if self.shortest_path_dist(id1, id2) == -1:
            return float('inf'), []
        if id1 == id2:
            ans_list.append(self.graph.getnode(id2))
            return 0.0, ans_list
        self.origin_all()
        dist_ans = self.dijkstra(self.graph.getnode(id1), self.graph.getnode(id2))
        src_node = self.graph.getnode(id1)
        dest_node = self.graph.getnode(id2)
        reverse_list = []
        temp = dest_node
        while temp.tag != -1:
            reverse_list.append(temp)
            temp = self.graph.getnode(temp.tag)
        ans_list.append(src_node.key)
        for i in range(len(reverse_list) - 1, -1, -1):
            ans_list.append(reverse_list[i].key)
        self.origin_all()
        return dist_ans, ans_list

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        ans_list = []
        copy_list = []
        dist = 0
        for n in node_lst:
            copy_list.append(n)
        first = copy_list.pop(0)
        ans_list.append(first)
        node_temp = None
        while len(copy_list) > 0:
            best = sys.float_info.max
            for n in copy_list:
                temp = self.shortest_path_dist(first, n)
                if temp < best:
                    best = temp
                    node_temp = n
            dist += best
            path = self.shortest_path(first, node_temp)
            for i in range(1, len(path[1]), 1):
                ans_list.append(path[1][i])
            copy_list.remove(node_temp)
            first = node_temp
        return ans_list, dist

    def centerPoint(self) -> (int, float):
        if not self.is_connected():
            return None, float('inf')
        center = None
        dist_ans = float('inf')
        for n in self.graph.nodes.values():
            self.origin_all()
            self.dijkstra_center(n.key)
            dist_temp = sys.float_info.min
            for k in self.graph.nodes.values():
                if k.weight > dist_temp:
                    dist_temp = k.weight
            if dist_temp < dist_ans:
                dist_ans = dist_temp
                center = n.key
        return center, dist_ans

    def shortest_path_dist(self, src: int, dest: int) -> float:
        self.origin_all()
        if self.graph.nodes.get(src) is None or self.graph.nodes.get(dest) is None:
            return -1
        if self.graph.edges.get(src) is None:
            return -1
        dist = self.dijkstra(self.graph.nodes.get(src), self.graph.nodes.get(dest))
        self.origin_all()
        if dist == sys.float_info.max:
            return -1
        return dist

    def dijkstra(self, src: Node, dest: Node):
        shortest = sys.float_info.max
        pq = PriorityQueue()
        src.weight = 0.0
        pq.insert(src)
        while not pq.is_empty():
            temp = pq.delete()
            if temp.info == "White":
                temp.info = "Black"
                if temp.key == dest.key:
                    return temp.weight
                # if self.graph.edges.get(temp.key) is not None:
                for e in self.graph.all_out_edges_of_node(temp.key):
                    edge = self.graph.edges[temp.key][e]
                    n = self.graph.getnode(edge.dst)
                    if n.info == "White":
                        if temp.weight + edge.weight < n.weight:
                            n.weight = temp.weight + edge.weight
                            n.tag = temp.key
                        pq.insert(n)
        return shortest

    def dijkstra_center(self, src: int):
        if self.graph.nodes.get(src) is None:
            return -1
        pq = PriorityQueue()
        for node in self.graph.nodes.values():
            if node.key == src:
                node.weight = 0.0
                node.tag = src
            else:
                node.weight = sys.float_info.max
                node.tag = -1
            pq.insert(node)
        while not pq.is_empty():
            temp_node = pq.delete()
            if self.graph.edges.get(temp_node.key) is not None:
                for edge in self.graph.edges.get(temp_node.key).values():
                    new_weight = temp_node.weight + edge.weight
                    if new_weight < self.graph.nodes.get(edge.dst).weight:
                        self.graph.nodes.get(edge.dst).weight = new_weight
                        self.graph.nodes.get(edge.dst).tag = temp_node.key
        return

        # if self.graph.nodes.get(str(src)) is None:
        #     return -1
        # pq = PriorityQueue()
        # for node in self.graph.nodes.values():
        #     if node.key == src:
        #         node.weight = 0
        #         node.tag = src
        #     else:
        #         node.weight = sys.float_info.max
        #         node.tag = -1
        #     pq.put(node)
        # while not pq.empty():
        #     temp_node = pq.get()
        #     if self.graph.edges.get(str(temp_node.key)) is not None:
        #         for edge in self.graph.edges.get(str(temp_node.key)).values():
        #             new_weight = temp_node.w + edge.weight
        #             if new_weight < self.graph.nodes.get(str(edge.dest)).w:
        #                 self.graph.nodes.get(str(edge.dest)).w = new_weight
        #                 self.graph.nodes.get(str(edge.dest)).tag = temp_node.key
        # return 1

    def origin_all(self):
        for n in self.graph.nodes.values():
            n.info = "White"
            n.tag = -1
            n.weight = sys.float_info.max

    def converse(self) -> DiGraph:
        converese_g = DiGraph()
        for n in self.graph.nodes.values():
            new_node = Node(n.key, (n.location.x, n.location.y, 0.0))
            converese_g.add_node(new_node.key)

        for d in self.graph.edges:
            for j in self.graph.edges.get(d).values():
                converese_g.add_edge(j.dst, j.src, j.weight)
        return converese_g

    def plot_graph(self) -> None:
        x_list = []
        y_list = []
        for node in self.graph.nodes.values():
            x_list.append(node.location.x)
            y_list.append(node.location.y)
        plt.plot(x_list, y_list, 'ro')
        for i in range(len(x_list)):
            plt.annotate(i, xy=(x_list[i], y_list[i]))
        for node_id in self.graph.get_all_v().keys():
            if self.graph.edges.get(node_id) is not None:
                edge_list = self.get_graph().all_out_edges_of_node(node_id)
                if edge_list is not None:
                    for edge in edge_list.keys():
                        src_x = self.get_graph().get_all_v().get(node_id).location.x
                        src_y = self.get_graph().get_all_v().get(node_id).location.y
                        dest_x = self.get_graph().get_all_v().get(edge).location.x
                        dest_y = self.get_graph().get_all_v().get(edge).location.y

                        plt.annotate("", xy=(src_x, src_y), xytext=(dest_x, dest_y),
                                     arrowprops={'arrowstyle': "<-"})
        plt.show()
        return True

    def __repr__(self):
        return "Graph: |V|= " + str(self.graph.v_size()) + ", |E|= " + str(self.graph.SizeOfEdge)
