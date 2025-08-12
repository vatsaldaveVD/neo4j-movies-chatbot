# graph.py
import os
import uuid
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))


def run_cypher(cypher_query):
    valid_keywords = ("MATCH", "CREATE", "MERGE", "RETURN", "WITH", "CALL")
    if not cypher_query.upper().startswith(valid_keywords):
        raise ValueError(f"Invalid Cypher query generated: {cypher_query}")

    with driver.session() as session:
        result = session.run(cypher_query)
        return list(result)


def create_session(session_id=None):
    if session_id is None:
        session_id = str(uuid.uuid4())
    query = """
    MERGE (s:Session {id: $session_id})
    RETURN s
    """
    with driver.session() as session:
        session.run(query, session_id=session_id)
    return session_id


def add_message(session_id, msg_type, content):
    """
    Adds a message to a session and updates LAST_MESSAGE link.
    Messages linked with NEXT relationships in sequence.
    """
    query = """
    MATCH (s:Session {id: $session_id})
    OPTIONAL MATCH (s)-[:LAST_MESSAGE]->(lastMsg:Message)
    CREATE (newMsg:Message {id: randomUUID(), type: $msg_type, content: $content})
    MERGE (s)-[r:LAST_MESSAGE]->(newMsg)
    DELETE r
    WITH s, lastMsg, newMsg
    FOREACH (_ IN CASE WHEN lastMsg IS NOT NULL THEN [1] ELSE [] END |
        CREATE (lastMsg)-[:NEXT]->(newMsg)
    )
    RETURN newMsg
    """
    with driver.session() as session:
        session.run(query, session_id=session_id, msg_type=msg_type, content=content)
