
import networkx as nx
import matplotlib.pyplot as plt

GRAPH_FILE = "schemes_graph.graphml"
OUTPUT_FILE = "schemes_graph_visualization.png"


def visualize_graph():
    # Load the existing knowledge graph
    graph = nx.read_graphml(GRAPH_FILE)

    print("Knowledge graph loaded successfully.")
    print("Nodes:", graph.number_of_nodes())
    print("Edges:", graph.number_of_edges())

    # Assign a color to each type of node
    colors = {
        "Scheme": "skyblue",
        "Department": "orange",
        "Beneficiary": "lightgreen",
        "Benefit": "pink",
        "ReviewStatus": "violet",
        "DataQuality": "gold",
    }

    node_colors = [
        colors.get(graph.nodes[node].get("node_type"), "lightgray")
        for node in graph.nodes()
    ]

    # Calculate node positions
    positions = nx.spring_layout(graph, seed=42, k=1.2)

    # Draw the graph
    plt.figure(figsize=(22, 16))

    nx.draw_networkx_edges(
        graph,
        positions,
        edge_color="gray",
        alpha=0.4,
        arrows=True,
        arrowsize=10,
    )

    nx.draw_networkx_nodes(
        graph,
        positions,
        node_color=node_colors,
        node_size=450,
        edgecolors="black",
        linewidths=0.5,
    )

    # Label only scheme nodes to keep the graph readable
    scheme_labels = {
        node: attributes.get("name", node)
        for node, attributes in graph.nodes(data=True)
        if attributes.get("node_type") == "Scheme"
    }

    nx.draw_networkx_labels(
        graph,
        positions,
        labels=scheme_labels,
        font_size=6,
    )

    plt.title("Tamil Nadu Government Schemes Knowledge Graph")
    plt.axis("off")
    plt.tight_layout()

    # Save the visualization as an image
    plt.savefig(OUTPUT_FILE, dpi=200, bbox_inches="tight")
    print("Visualization saved to:", OUTPUT_FILE)

    plt.show()


if __name__ == "__main__":
    visualize_graph()
