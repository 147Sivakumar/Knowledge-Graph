
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
database = os.getenv("NEO4J_DATABASE", "neo4j")

if not all([uri, username, password]):
    raise ValueError(
        "Missing Neo4j credentials. Check your .env file."
    )

try:
    with GraphDatabase.driver(
        uri,
        auth=(username, password)
    ) as driver:
        driver.verify_connectivity()

        records, summary, keys = driver.execute_query(
            "RETURN 'AuraDB connected successfully!' AS message",
            database_=database,
        )

        print("\nSUCCESS:", records[0]["message"])

except Exception as error:
    print("\nCONNECTION FAILED")
    print("Error type:", type(error).__name__)
    print("Details:", error)
