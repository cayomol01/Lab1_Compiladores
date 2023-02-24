import matplotlib.pyplot as plt
import networkx as nx


def Graph(edges, edgesLabel, estadoAceptacion, estadoInicial):

    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    plt.figure()
    colores = []

    for nodo in G.nodes:
            # print(nodo)
            colores.append('lightgreen' if nodo == 'q0' else  "pink" if nodo== estadoAceptacion else   'lightblue')
            

    nx.draw(
        G, pos, edge_color='black', width=1, linewidths=1, node_color=colores,
        node_size=500, alpha=0.9,
        labels={node: node for node in G.nodes()}
    )
    # nx.draw_networkx(G, node_color=colores, with_labels=True)

    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edgesLabel,
        font_color='red'
    )

    plt.show()