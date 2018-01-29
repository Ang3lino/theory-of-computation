from DirectedGraph import *

g = DirectedGraph()

def test1():
    g.add_edge('a', 'b')
    g.add_edge('b', 'f')
    g.add_edge('c', 'd')
    g.add_edge('d', 'h')
    g.add_edge('f', 'd')
    g.add_edge('f', 'i')
    g.add_edge('g')
    g.add_edge('i', 'e')
    g.add_edge('e', 'e')

    print('g.out_edges')
    for a in { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i' }:
        print(a)
        print(g.out_edges(a))

def test2():
    g.add_edge('s', 'b')
    g.add_edge('b', 'a')
    g.add_edge('a', 'b')
    for a in { 's', 'a', 'b' }:
        print(a)
        print(g.out_edges(a))

test2()