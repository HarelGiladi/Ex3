import json
from typing import List

from matplotlib import pyplot as plt

from src import DiGraph
from src.Node import Node
from src.api.GraphAlgoInterface import GraphAlgoInterface
from src.api.GraphInterface import GraphInterface


  #need to be change!!
class GraphAlgo(GraphAlgoInterface):
    def __init__(self, g: DiGraph = DiGraph()) -> None:
        self.graph = g

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        with open(file_name, 'r') as f:
            data = json.load(f)
        l_nodes = data["Nodes"]
        l_edges = data["Edges"]
        for dic_nodes in l_nodes:
            pos = dic_nodes["pos"].split(',')
            self.graph.add_node(dic_nodes['id'], (float(pos[0]), float(pos[1]), float(pos[2])))
        for dic_edges in l_edges:
            self.graph.add_edge(dic_edges['src'], dic_edges['dest'], dic_edges['w'])
        return True

    def save_to_json(self, file_name: str) -> bool:
        graph_dic = {'Nodes': self.graph.get_list_nodes(), 'Edges': self.graph.get_list_edges()}
        with open(file_name, 'w') as json_file:
            json.dump(graph_dic, json_file)
        return True

    def Dijkstra(self, src: Node, dest: Node):
        shortest = 1000000
        queue = []
        src.setweight(0.0)
        queue.append(src)
        while len(queue) != 0:
            queue.sort()
            temp = queue.pop(0)
            if temp.getinfo() == "White":
                temp.setinfo("Black")
                if temp.getkey() == dest.getkey():
                    return temp.getweight()
                for e in self.graph.all_out_edges_of_node(temp.getkey()):
                    ed = self.graph.edges[temp.getkey()][e]
                    no = self.graph.getnode(e)
                    if no.info == "White":
                        if temp.getweight() + ed.getweight() < no.getweight():
                            no.setweight(temp.getweight() + ed.getweight())
                            no.settag(temp.getkey())
                        queue.append(no)
        return shortest

    def reset(self):
        for n in self.graph.nodes.values():
            n.setinfo("White")
            n.settag(-1)
            n.setweight(1000000)

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        ans = []
        ansdist = self.shortest_path_dist(id1, id2)
        if ansdist == -1:  # shode to throw exsepion
            return None
        if id1 == id2:
            return (0, [])
        self.reset()
        self.Dijkstra(self.graph.getnode(id1), self.graph.getnode(id2))
        Nsrc = self.graph.getnode(id1)
        Ndest = self.graph.getnode(id2)
        revers = []
        temp = Ndest
        while temp.gettag() != -1:
            revers.append(temp)
            temp = self.graph.getnode(temp.gettag())
        ans.append(Nsrc)

        for i in range(len(revers) - 1, 0, -1):
            ans.append(revers[i])
        self.reset()
        return (ansdist, ans)

    def shortest_path_dist(self, src: int, dest: int) -> float:
        self.reset()
        ans = self.Dijkstra(self.graph.get_all_v().get(src), self.graph.get_all_v().get(dest))
        self.reset()
        if ans == 1000000:
            return -1
        return ans

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        al = []
        path = []
        copy = []
        for n in node_lst:
            copy.append(n)
        first = copy.pop(0)
        al.append(first)
        while len(copy) > 0:
            best = 1000000
            for nod in copy:
                temp = self.shortest_path_dist(first, nod)
                if temp < best:
                    best = temp
                    Ntemp = nod
            path = self.shortest_path(first, Ntemp)

            for i in range(0, len(path), 1):
                al.append(path[i])
            copy.remove(Ntemp)
            first = Ntemp
        return al

    def centerPoint(self) -> (int, float):
        max = 0
        min = 0
        center = 0
        magic = Node(-1, (0, 0, 0))
        distans = 1000000
        ass = 0
        for nod in self.graph.nodes.values():
            n = nod
            self.reset()
            self.Dijkstra(n, magic)
            distemp = -1000000
            for tempn in self.graph.nodes.values():
                k = tempn
                if k.getweight() > distemp:
                    distemp = k.getweight()
            if distemp < distans:
                distans = distemp
                center = n.getkey()
            if ass == 0:
                min = nod.getkey()
            if ass == self.graph.v_size() - 1:
                max = nod.getkey()
            ass = ass + 1
        ansdist = self.shortest_path_dist(max, min)
        return center, ansdist

    def plot_graph(self) -> None:
        for src in self.graph.nodes.values():
            x, y, z = src.pos
            plt.plot(x, y, markersize=10, marker="o", color="red")
            plt.text(x, y, str(src.key), color="blue", fontsize=12)

            for dest in self.graph.edges[src.key]:
                n_x, n_y, n_z = self.graph.nodes[dest].pos
                plt.annotate("", xy=(x, y), xytext=(n_x, n_y), arrowprops=dict(arrowstyle="<-"))
        plt.show()