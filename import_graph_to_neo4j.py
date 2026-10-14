
import os
import networkx as nx
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

GRAPH_FILE = "schemes_graph.graphml"

# Load your existing NetworkX graph
G = nx.read_graphml(GRAPH_FILE)

print("Graph loaded successfully")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())


def clean_properties(properties):
    """Convert GraphML properties to Neo4j-compatible values."""
    result = {}

    for key, value in properties.items():
        if value is None:
            continue

        key = str(key)
        if not key or key.startswith("_"):
            continue

        if isinstance(value, (str, int, float, bool)):
            result[key] = value
        elif isinstance(value, (list, tuple)):
            if all(isinstance(v, (str, int, float, bool))
                   for v in value):
                result[key] = list(value)

    return result


if not all([URI, USERNAME, PASSWORD]):
    raise ValueError("Check your Neo4j credentials in .env")

# Import nodes and relationships
with GraphDatabase.driver(
    URI, auth=(USERNAME, PASSWORD)
) as driver:

    driver.verify_connectivity()

    with driver.session(database=DATABASE) as session:

        # Create a stable unique key for imported graph nodes
        session.run("""
            CREATE CONSTRAINT imported_node_id IF NOT EXISTS
            FOR (n:ImportedNode)
            REQUIRE n.graph_id IS UNIQUE
        """).consume()

        # Import nodes in batches
        nodes = [
            {
                "graph_id": str(node_id),
                "properties": clean_properties(dict(attrs)),
            }
            for node_id, attrs in G.nodes(data=True)
        ]

        for start in range(0, len(nodes), 500):
            batch = nodes[start:start + 500]

            session.run("""
                UNWIND $rows AS row
                MERGE (n:ImportedNode {graph_id: row.graph_id})
                SET n += row.properties
            """, rows=batch).consume()

        # Import relationships in batches
        edges = []

        for source, target, attrs in G.edges(data=True):
            edges.append({
                "source": str(source),
                "target": str(target),
                "properties": clean_properties(dict(attrs)),
            })

        for start in range(0, len(edges), 500):
            batch = edges[start:start + 500]

            session.run("""
                UNWIND $rows AS row
                MATCH (a:ImportedNode {graph_id: row.source})
                MATCH (b:ImportedNode {graph_id: row.target})
                MERGE (a)-[r:CONNECTED_TO]->(b)
                SET r += row.properties
            """, rows=batch).consume()

    # Verify the imported graph
    records, _, _ = driver.execute_query("""
        MATCH (n:ImportedNode)
        RETURN count(n) AS nodes
    """, database_=DATABASE)

    print("Neo4j nodes:", records[0]["nodes"])

    records, _, _ = driver.execute_query("""
        MATCH (:ImportedNode)-[r:CONNECTED_TO]->(:ImportedNode)
        RETURN count(r) AS relationships
    """, database_=DATABASE)

    print("Neo4j relationships:", records[0]["relationships"])

print("Graph import completed!")
