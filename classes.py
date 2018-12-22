#!/usr/bin/env python3

from collections import deque
import hashlib
import subprocess as sp

class State:
    def __init__(self):
        self.nodes = {}  # id: Node object
        self.__queue = deque()  # ids. Subset of self.nodes

    def __repr__(self):
        return "Nodes: " + str(self.nodes.values()) + "\n" + "Queue: " + str(self.__queue)

    def enqueue(self, node, to_left=False):
        assert isinstance(node, Node)
        if node.id in self.nodes:
            self.nodes[node.id].parent_ids |= node.parent_ids
            return
        self.nodes[node.id] = node
        if to_left:
            self.__queue.appendleft(node.id)
        else:
            self.__queue.append(node.id)

    def non_empty_queue(self):
        return (len(self.__queue) > 0)

    def pop(self, noremove=False):
        if noremove:
            return self.__queue[0]
        else:
            return self.__queue.popleft()

    def delete_by_id(self, did):
        if did in self.nodes:
            del self.nodes[did]
        if did in self.__queue:
            self.__queue.remove(did)
        for node in self.nodes.values():
            if did in node.parent_ids:
                node.parent_ids.remove(did)

    def name_exists(self, name):
        nameset = {node.name for node in self.nodes.values()}
        return name in nameset

    def id_by_name(self, name):
        for n in self.nodes.values():
            if n.name == name:
                return n.id
        else:
            raise ValueError("Not found")

    def save_graph(self, keep_dot=False):
        if self.non_empty_queue():
            topid = self.pop(noremove=True)
        else:
            topid = None
        st = "digraph {\n"
        st += "rankdir=LR;\n"
        for id in self.nodes:
            n = self.nodes[id]
            suff = 'fillcolor = "#ccccff", style = filled, ' if n.id == topid else ""
            st += f'i{n.id} [{suff} label = "{n.name}"];\n'
            for pid in n.parent_ids:
                pn = self.nodes[pid]
                st += f"i{pn.id} -> i{n.id};\n"
        st += "}\n"
        with open("tmp.dot", "w") as f:
            f.write(st)
        sp.run("dot -Tpng tmp.dot -o graph.png", shell=True, check=True)
        if not keep_dot:
            sp.run("rm -f tmp.dot", shell=True, check=True)

    def merge_names(self, name_from, name_to):
        fid = self.id_by_name(name_from)
        tid = self.id_by_name(name_to)
        self.nodes[tid].parent_ids |= self.nodes[fid].parent_ids
        for node in self.nodes.values():
            if fid in node.parent_ids:
                node.parent_ids.remove(fid)
                node.parent_ids.add(tid)
        if tid != fid:
            self.delete_by_id(fid)
        self.delete_self_reference()

    def delete_self_reference(self):
        for node in self.nodes.values():
            if node.id in node.parent_ids:
                node.parent_ids.remove(node.id)

    def html_nodes(self):
        st = ""
        for q in self.nodes.values():
            st += str(q) + "<br>\n"
        return st

    def html_queue(self):
        st = ""
        for q in self.__queue:
            assert q in self.nodes
            st += self.nodes[q].name + "<br>\n"
        return st

class Node:
    def __init__(self, id, name, parent_ids):
        self.id = id
        self.name = name
        self.parent_ids = parent_ids

    def __repr__(self):
        pts = " ".join([f"{i:4.4s}" for i in self.parent_ids])
        return f"{self.name} (id: {self.id:4.4s}, parents: [{pts}])"

