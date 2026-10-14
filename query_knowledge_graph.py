
import networkx as nx

GRAPH_FILE = "schemes_graph.graphml"


def load_graph():
    return nx.read_graphml(GRAPH_FILE)


def search_schemes(graph, search_text):
    search_text = search_text.lower().strip()
    found = 0

    for node_id, data in graph.nodes(data=True):
        if data.get("node_type") != "Scheme":
            continue

        name = data.get("name", "")
        if search_text not in name.lower():
            continue

        found += 1
        print(f"\nScheme: {name}")
        print("Source:", data.get("source_url", ""))
        print("Review status:", data.get("review_status", ""))

        for _, target, edge in graph.out_edges(node_id, data=True):
            target_data = graph.nodes[target]
            node_type = target_data.get("node_type", "")
            target_name = target_data.get("name", "")
            relationship = edge.get("relationship", "")

            print(f"  {relationship}: {target_name} ({node_type})")

    if found == 0:
        print("No matching schemes found.")

    print(f"\nMatching schemes: {found}")


def show_review_schemes(graph):
    found = 0

    for node_id, data in graph.nodes(data=True):
        if data.get("node_type") != "Scheme":
            continue

        if data.get("review_status") != "Needs manual review":
            continue

        found += 1
        print(f"\n{found}. {data.get('name', '')}")
        print("   Source:", data.get("source_url", ""))

    print(f"\nSchemes requiring review: {found}")


def main():
    graph = load_graph()

    while True:
        print("\n===== Tamil Nadu Schemes Knowledge Graph =====")
        print("1. Search schemes by name")
        print("2. Show schemes flagged for review")
        print("3. Show graph statistics")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            search_text = input("Enter part of a scheme name: ")
            search_schemes(graph, search_text)

        elif choice == "2":
            show_review_schemes(graph)

        elif choice == "3":
            schemes = sum(
                1 for _, data in graph.nodes(data=True)
                if data.get("node_type") == "Scheme"
            )
            print("Schemes:", schemes)
            print("Graph nodes:", graph.number_of_nodes())
            print("Relationships:", graph.number_of_edges())

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
