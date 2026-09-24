from neo4j import GraphDatabase

from config import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
    NEO4J_DATABASE
)


driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)


def test_connection():

    with driver.session(database=NEO4J_DATABASE) as session:

        result = session.run(
            "RETURN 'MediSynth Neo4j Connected' AS message"
        )

        return result.single()["message"]