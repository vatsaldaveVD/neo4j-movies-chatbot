from llm import generate_cypher
from graph import run_cypher
from utils import format_results


def chatbot_answer(user_question):
    try:
        cypher_raw = generate_cypher(user_question)
        cypher = clean_cypher(cypher_raw)  # Clean before running
        results = run_cypher(cypher)
        answer = format_results(results)
        return answer, cypher
    except Exception as e:
        return f"Error: {str(e)}", None


def clean_cypher(cypher_raw: str) -> str:
    lines = cypher_raw.strip().splitlines()
    lines = [
        line
        for line in lines
        if not (line.strip().startswith("```") or line.strip().endswith("```"))
    ]
    return "\n".join(lines).strip()
