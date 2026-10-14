

import networkx as nx

GRAPH_FILE = "schemes_graph.graphml"


def load_graph():
    """Load the existing NetworkX graph."""
    return nx.read_graphml(GRAPH_FILE)


def find_related_schemes(question, graph, limit=5):
    """Find matching schemes and retrieve their connected graph facts."""
    question_words = {
        word.lower().strip(".,?!:;()[]")
        for word in question.split()
        if len(word) > 2
    }

    matches = []

    for node, attributes in graph.nodes(data=True):
        if attributes.get("node_type") != "Scheme":
            continue

        scheme_name = attributes.get("name", "")
        name_words = {
            word.lower().strip(".,?!:;()[]")
            for word in scheme_name.split()
            if len(word) > 2
        }

        score = len(question_words & name_words)

        if score > 0:
            matches.append((score, node, attributes))

    matches.sort(key=lambda item: item[0], reverse=True)

    results = []

    for score, scheme_node, attributes in matches[:limit]:
        facts = {
            "scheme": attributes.get("name", ""),
            "source_url": attributes.get("source_url", ""),
            "review_status": attributes.get("review_status", "Unknown"),
            "relationships": [],
        }

        for _, target, edge_attributes in graph.out_edges(
            scheme_node, data=True
        ):
            target_attributes = graph.nodes[target]

            facts["relationships"].append({
                "relationship": edge_attributes.get(
                    "relationship", "RELATED_TO"
                ),
                "node_type": target_attributes.get(
                    "node_type", "Unknown"
                ),
                "name": target_attributes.get("name", target),
            })

        results.append(facts)

    return results


if __name__ == "__main__":
    graph = load_graph()

    print("Knowledge graph loaded.")
    print("Nodes:", graph.number_of_nodes())
    print("Edges:", graph.number_of_edges())

    question = input("\nEnter a scheme name or keyword to search: ")
    results = find_related_schemes(question, graph)

    if not results:
        print("No matching schemes found.")
    else:
        for item in results:
            print("\nScheme:", item["scheme"])
            print("Review status:", item["review_status"])

            for fact in item["relationships"]:
                print(
                    f"  {fact['relationship']}: "
                    f"{fact['name']} ({fact['node_type']})"
                )

            print("Source:", item["source_url"])
