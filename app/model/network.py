# -*- coding: utf-8 -*
import networkx as nx
import matplotlib.pyplot as plt


def make_graph():
    G = nx.Graph()

    # add nodes
    G.add_node('Rechtbank Amsterdam')
    G.add_node('Curator A')
    G.add_node('Curator A')
    G.add_node('Zaak A1')
    G.add_node('Zaak A2')

    # add edges
    G.add_edge('Rechtbank Amsterdam', 'Curator A')
    G.add_edge('Rechtbank Amsterdam', 'Curator B')
    G.add_edge('Curator A', 'Zaak A1')
    G.add_edge('Curator A', 'Zaak A2')

    print('no nodes %d' % G.number_of_nodes())
    print('no edges %d' % G.number_of_edges())

    # set edge properties
    G['Rechtbank Amsterdam']['Curator A']['color'] = 1000
    print(G['Rechtbank Amsterdam']['Curator A'])

    nx.draw(G)
    plt.show()
    #plt.savefig("path.png")

if __name__ == "__main__":
    make_graph()
