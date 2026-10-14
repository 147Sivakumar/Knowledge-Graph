
import os
import re
import networkx as nx

from dotenv import load_dotenv
from neo4j import GraphDatabase
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

if not all([URI, USERNAME, PASSWORD]):
    raise ValueError("Check Neo4j credentials in your .env file")

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is missing from your .env file")

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a government schemes GraphRAG assistant.
Use only the retrieved knowledge graph evidence.
Do not invent scheme names, eligibility, benefits, or amounts.
Explain the facts supporting your answer.
If evidence is insufficient, say so clearly."""),
    ("human", """Question: {question}

Retrieved graph evidence:
{context}

Answer clearly and helpfully."""),
])

chain = prompt | llm


def retrieve_graph(question):
    terms = list({
        word.lower()
        for word in re.findall(r"\b\w+\b", question)
        if len(word) > 2
    })

    query = """
    MATCH (n:ImportedNode)
    WITH n,
         toLower(coalesce(n.graph_id, '') + ' ' +
         reduce(s = '', k IN keys(n) |
             s + ' ' + toString(n[k]))) AS searchable
    WHERE any(word IN $terms WHERE searchable CONTAINS word)
    WITH n
    LIMIT 5

    OPTIONAL MATCH (n)-[r:CONNECTED_TO]-(neighbor:ImportedNode)

    RETURN n.graph_id AS node_id,
           properties(n) AS node_properties,
           collect(DISTINCT {
               direction: CASE
                   WHEN startNode(r) = n THEN 'OUTGOING'
                   ELSE 'INCOMING'
               END,
               relationship: type(r),
               properties: properties(r),
               neighbor_id: neighbor.graph_id,
               neighbor_properties: properties(neighbor)
           }) AS connections
    """

    with GraphDatabase.driver(
        URI, auth=(USERNAME, PASSWORD)
    ) as driver:
        records, _, _ = driver.execute_query(
            query, terms=terms, database_=DATABASE
        )

    facts = []
    for record in records:
        facts.append({
            "node_id": record["node_id"],
            "properties": record["node_properties"],
            "connections": [
                c for c in record["connections"]
                if c["neighbor_id"] is not None
            ],
        })

    return facts



def analyze_with_networkx(facts):
    graph = nx.DiGraph()

    for fact in facts:
        node_id = fact["node_id"]
        graph.add_node(node_id, **(fact["properties"] or {}))

        for connection in fact["connections"]:
            neighbor_id = connection["neighbor_id"]

            if connection["direction"] == "OUTGOING":
                source, target = node_id, neighbor_id
            else:
                source, target = neighbor_id, node_id

            graph.add_node(
                neighbor_id,
                **(connection["neighbor_properties"] or {})
            )

            edge_properties = connection["properties"] or {}
            edge_properties["relationship"] = connection["relationship"]

            graph.add_edge(source, target, **edge_properties)

    print(
        f"\nRetrieved subgraph: {graph.number_of_nodes()} nodes, "
        f"{graph.number_of_edges()} relationships"
    )

    return graph




def answer_question(question, history=None):
    history_text = "\n".join(history[-6:]) if history else ""

    search_text = (
        history_text + "\nCurrent question: " + question
    )
    facts = retrieve_graph(search_text)

    if not facts:
        return (
            "I couldn't find matching graph evidence. "
            "Try a scheme name, department, or benefit keyword."
        )

    graph = analyze_with_networkx(facts)

    context_lines = []

    for node, properties in graph.nodes(data=True):
        context_lines.append(
            f"NODE: {node}; PROPERTIES: {properties}"
        )

    for source, target, properties in graph.edges(data=True):
        context_lines.append(
            f"RELATIONSHIP: {source} -> {target}; "
            f"PROPERTIES: {properties}"
        )

    context = "\n".join(context_lines)

    response = chain.invoke({
        "question": question,
        "history": history_text or "No previous conversation.",
        "context": context,
    })

    return response.content



def main():
    print("Connecting to Neo4j AuraDB...")

    with GraphDatabase.driver(
        URI, auth=(USERNAME, PASSWORD)
    ) as driver:
        driver.verify_connectivity()

        records, _, _ = driver.execute_query(
            "MATCH (n:ImportedNode) RETURN count(n) AS total_nodes",
            database_=DATABASE,
        )

        print("Neo4j nodes:", records[0]["total_nodes"])

    print("\nLangChain GraphRAG chatbot is ready!")
    print("Type 'exit' to stop.\n")

    while True:
        try:
            question = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nChatbot stopped.")
            break

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            print("\nAssistant:", answer_question(question), "\n")
        except Exception as error:
            print(f"\nError: {type(error).__name__}: {error}\n")


if __name__ == "__main__":
    main()
