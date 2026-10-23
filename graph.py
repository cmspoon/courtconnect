import webbrowser
from pyvis.network import Network
import networkx as nx

def display_graph(graph, discovered_nodes, start, target, auto_open=True):
    net = Network(height="750px", width="100%", bgcolor="#1a1a1a", font_color="white", directed=False)
    net.barnes_hut(gravity=-3000, central_gravity=0.3, spring_length=120, spring_strength=0.05, damping=0.09)

    # Build internal graph to analyze components
    G = nx.Graph()
    for node in discovered_nodes:
        G.add_node(node)
    for u, neighbors in graph.items():
        for v in neighbors:
            G.add_edge(u, v)

    start_comp = nx.node_connected_component(G, start) if start in G else set()
    target_comp = nx.node_connected_component(G, target) if target in G else set()

    # Add nodes with hierarchical colors
    for node in discovered_nodes:
        if node == start:
            net.add_node(node, label=f"START: {node}", color="#4CAF50", size=30, shape="dot")
        elif node == target:
            net.add_node(node, label=f"TARGET: {node}", color="#F44336", size=30, shape="dot")
        elif node in start_comp or node in target_comp:
            # Connected to Start or Target
            net.add_node(node, label=node, color="#FF9800", size=22, shape="dot")
        elif G.degree[node] > 0:
            # Independent clusters
            net.add_node(node, label=node, color="#2196F3", size=18, shape="dot")
        else:
            # Isolated floating nodes
            net.add_node(node, label=node, color="#757575", size=14, shape="dot")

    # Add teammate connection edges
    added_edges = set()
    for u, neighbors in graph.items():
        for v in neighbors:
            edge_key = tuple(sorted([u, v]))
            if edge_key not in added_edges:
                net.add_edge(u, v, color="#555555", width=2)
                added_edges.add(edge_key)

    html_file = "journeyman.html"
    net.write_html(html_file, open_browser=False)

    if auto_open:
        webbrowser.open(html_file)