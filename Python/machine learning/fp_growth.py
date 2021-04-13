import pandas as pd
import numpy as np
import string

from collections import defaultdict
from itertools import combinations
from graphviz import Digraph
from typing import DefaultDict, List, Tuple


class MyFPGrowth:
    def __init__(self, lst_itemsets: List[List[str]], minsup: float):
        self.lst_items, self.dic_items = preprocessing(lst_itemsets)
        self.encoding_data = encoding(lst_itemsets, self.dic_items)
        self.frequence_table = frequence(
            self.encoding_data, self.lst_items, len(self.lst_items))
        self.tree = None
        self.minsup = minsup

    def initOrderedItemsets(self):
        self.minsup_frequence_table = initOrderedFrequenceTable(
            self.frequence_table['0'], len(self.encoding_data), self.minsup)
        self.ordered_itemsets = initOrderedItemsets(
            self.encoding_data, self.minsup_frequence_table.index.tolist())

    def genFpTree(self):
        self.initOrderedItemsets()
        self.tree = Tree()

        for itemset in self.ordered_itemsets:
            self.tree.addItemset(itemset)

    def drawTree(self, export_png: str = None):
        if self.tree is not None:
            dot = self.tree.drawTree(self.lst_items)

            if export_png is not None:
                dot.format = 'png'
                dot.render(export_png, view=False)

            return dot

    def associationRules(self):
        table = []
        for i in self.minsup_frequence_table[::-1].index:
            row = [i]
            patterns = []
            for leaf in self.tree.items_pos[i]:
                node = leaf.parent
                path = []

                while node.id != -1:
                    path.append(node.id)
                    node = node.parent

                path.append(leaf.count)
                patterns.append(path)

            row.append(patterns)
            table.append(row)

        table = genSamples(table, self.minsup, len(self.encoding_data))
        res = []

        for a, b in zip(self.minsup_frequence_table[::-1].index, table):
            line = [self.lst_items[a]]
            samples = []

            for itemset in b:
                samples.append(tuple([self.lst_items[item]
                                      for item in itemset]))

            line.append(samples)
            res.append(line)

        return pd.DataFrame(res, columns=['alpha', 'patterns'])


def preprocessing(itemsets: List[List[str]]):
    lst_items = list(set([item for itemset in itemsets for item in itemset]))
    dic_items: DefaultDict[str, int] = defaultdict(int)

    for val, key in enumerate(lst_items):
        dic_items[key] = val

    return lst_items, dic_items


def encoding(itemsets: List[List[str]], dic_items: DefaultDict[str, int]):
    itemsets_encoding = []

    for itemset in itemsets:
        row = [dic_items[item] for item in itemset]
        itemsets_encoding.append(row)

    return itemsets_encoding


def frequence(itemsets: List[List[int]], lst_items, n: int):
    freq: np.ndarray = np.zeros(n, dtype=int)

    for itemset in itemsets:
        mask = list(set(itemset))
        freq[mask] += 1

    df = pd.DataFrame()
    df['0'] = freq
    df['1'] = [lst_items[i] for i in range(n)]

    return df.sort_values(['0', '1'], ascending=(False, True))


def initOrderedFrequenceTable(frequen_table: pd.Series, no_rows: int, minsup: float):
    new_frequence_table = frequen_table[frequen_table/no_rows >= minsup]

    return new_frequence_table


def initOrderedItemsets(encoding_itemsets: List[List[int]], itemset: List[int]):
    set_itemset = set(itemset)
    odered_itemsets: List[List[int]] = []

    for itemset_ in encoding_itemsets:
        row = sorted(set_itemset & set(itemset_), key=itemset.index)
        odered_itemsets.append(row)

    return odered_itemsets


class Node:
    def __init__(self, id: int, label: str, parent: 'Node'):
        self.count = 0
        self.label = label
        self.child = {}
        self.id = id
        self.parent = parent


class Tree:
    def __init__(self):
        self.root = Node(-1, '0', None)
        self.items_pos = {}
        self.label = 1

    def addItemset(self, itemset: List[int]):
        tmp = self.root
        chars = string.digits + string.ascii_letters + string.punctuation

        for item in itemset:
            if tmp.child.get(item) is None:
                tmp.child[item] = Node(item, chars[self.label], tmp)
                self.label += 1

                if self.items_pos.get(item) is None:
                    self.items_pos[item] = [tmp.child[item]]
                else:
                    self.items_pos[item].append(tmp.child[item])

            tmp.child[item].count += 1
            tmp = tmp.child.get(item)

    def drawTree(self, lst_items: List[str]):
        dot = Digraph()
        lst_nodes, lst_edges = [], []
        prepareTree(-1, self.root, lst_nodes, lst_edges, lst_items)
        lst_nodes[0] = ('0', 'Root')

        for node in lst_nodes:
            dot.node(node[0], node[1])

        dot.edges(lst_edges)

        for key, items in self.items_pos.items():
            if len(items) > 1:
                for j in range(1, len(items)):
                    a = items[j - 1]
                    b = items[j]
                    dot.edge(a.label, b.label, constraint='false',
                             style='dashed', color='gray')

        return dot


def prepareTree(node_pos: int, node: Node, lst_nodes: List[Tuple[str, str]], lst_edges: List[str], lst_items: List[str]):
    lst_nodes.append((node.label, f'{lst_items[node_pos]}:{node.count}'))

    for key, item in node.child.items():
        lst_edges.append(f'{node.label}{item.label}')
        prepareTree(key, item, lst_nodes, lst_edges, lst_items)


def genSamples(table: List[List], minsup: float, n: int):
    res = []

    for row in table:
        beta = row[0]
        d = defaultdict(int)
        tmp = [beta]

        for itemset in row[1]:
            for item in itemset[:-1]:
                d[item] = d.get(item, 0) + itemset[-1]

        tmp.append(d)
        items = []
        for key, val in d.items():
            if val/n >= minsup:
                items.append(key)

        tmp1 = sum([list(map(list, combinations(items, i)))
                    for i in range(len(items) + 1)], [])
        samples = [[beta] + arr for arr in tmp1]

        res.append(samples)

    return res
