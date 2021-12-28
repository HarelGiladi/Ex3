from api import GraphInterface
from src.Edge import Edge
from src.GLocation import GLocation
from src.Node import Node


class DiGraph(GraphInterface):
    def __init__(self) -> None:
        self.nodes = {}
        self.edges = {}
        self.SizeOfEdge = 0
        self.list_nodes = []
        self.list_edges = []
        self.MC = 0

    def v_size(self) -> int:
        return len(self.nodes)

    def e_size(self) -> int:
        return self.SizeOfEdge

    def get_all_v(self) -> dict:
        return self.nodes

    def get_list_nodes(self) -> list:
        return self.list_nodes

    def get_list_edges(self) -> list:
        return self.list_edges

    def all_in_edges_of_node(self, id1: int) -> dict:
        ans = {}
        count = 0
        for i in self.edges.keys():
            for j in self.edges[i].keys():
                # if j == id1:
                #     if i not in ans.keys():
                #         ans[i] = self.edges[i][id1]
                if j ==id1 & i not in ans.keys():
                    ans[count]=self.edges[i][id1]
                    count+=1
        return ans

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.edges[id1]

    def get_mc(self) -> int:
        return self.MC

    # id1 - src , id2 - dst
    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self.nodes.keys() or id2 not in self.nodes.keys():
            return False
        edge = Edge(id1, id2, weight)
        if id1 in self.edges.keys():
            if id2 in self.edges[id1].keys():
                return False
            else:
                self.edges[id1][id2] = edge
                self.SizeOfEdge += 1
        else:
            self.edges[id1] = {id2: edge}
            self.SizeOfEdge += 1

        self.list_edges.append({'src': id1, 'dest': id2, 'w': weight})
        self.MC +=1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self.nodes.keys():
            return False
        else:
            temp = GLocation(pos)
            self.nodes[node_id] = Node(node_id, temp)

        self.list_nodes.append({'id': node_id, 'pos': pos})
        self.MC = self.MC + 1
        return True

    def getnode(self, id: int) -> Node:
        #if self.nodes[id]:
        return self.nodes[id]
        #return None

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self.nodes.keys():
            return False
        else:
            # remove from nodes
            self.nodes.pop(node_id)

        # remove all the edges from the node
        if node_id in self.edges.keys():
            self.edges.pop(node_id)
            self.list_edges.pop(node_id)
        # remove all the edges into the node
        for id1 in self.edges.keys():
            for id2 in self.edges[id1].keys():
                if id2 == node_id:
                    self.edges[id1].pop(node_id)
                    self.list_edges[id1].pop(node_id)
                    self.SizeOfEdge -= 1

        self.MC +=1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 not in self.edges.keys() or node_id2 not in self.edges.keys():
            return False
        if node_id1 in self.edges.keys() and node_id2 not in self.edges[node_id1].keys():
            return False
        else:
            self.edges[node_id1].pop(node_id2)
            for i in self.list_edges:
                if i['src'] == node_id1 and i['dest'] == node_id2:
                    self.list_edges.remove(i)
                    break
            # self.list_edges[node_id1].pop(node_id2)
            self.SizeOfEdge -= 1
        self.MC = self.MC + 1
        return True
