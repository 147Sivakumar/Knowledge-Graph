
import os
import networkx as nx
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

if not all([URI, USERNAME, PASSWORD]):
    raise ValueError("Check your Neo4j credentials in .env")

G = nx.DiGraph()

with GraphDatabase.driver(
    URI, auth=(USERNAME, PASSWORD)
) as driver:
    driver.verify_connectivity()

    records, _, _ = driver.execute_query(
        """
        MATCH (n:ImportedNode)
        RETURN n.graph_id AS id, properties(n) AS props
        """,
        database_=DATABASE,
    )

    for record in records:
        node_id = record["id"]
        properties = record["props"]
        G.add_node(node_id, **properties)

    records, _, _ = driver.execute_query(
        """
        MATCH (a:ImportedNode)-[r:CONNECTED_TO]->(b:ImportedNode)
        RETURN a.graph_id AS source,
               b.graph_id AS target,
               properties(r) AS props
        """,
        database_=DATABASE,
    )

    for record in records:
        G.add_edge(
            record["source"],
            record["target"],
            **record["props"],
        )

print("Graph retrieved from Neo4j AuraDB")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# Save a local NetworkX copy
nx.write_graphml(G, "schemes_graph_from_neo4j.graphml")

# Draw the graph
plt.figure(figsize=(18, 12))

pos = nx.spring_layout(G, seed=42, k=0.8)

nx.draw_networkx_nodes(
    G, pos,
    node_size=450,
    node_color="skyblue",
)

nx.draw_networkx_edges(
    G, pos,
    edge_color="gray",
    arrows=True,
    arrowsize=12,
)

nx.draw_networkx_labels(
    G, pos,
    labels={node: str(node) for node in G.nodes()},
    font_size=6,
)

plt.title("Knowledge Graph Retrieved from Neo4j AuraDB")
plt.axis("off")
plt.tight_layout()

plt.savefig(
    "schemes_graph_from_neo4j.png",
    dpi=200,
    bbox_inches="tight",
)

plt.show()
print("Saved schemes_graph_from_neo4j.graphml")
print("Saved schemes_graph_from_neo4j.png")
