# llm.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_CHAT = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
MODEL_CYPHER = "gpt-4o-mini"

client = OpenAI(api_key=OPENAI_API_KEY)

SCHEMA_AND_SAMPLES = """
You are an expert in Neo4j Cypher querying. Below is the schema and example data from the graph database.

--- SCHEMA ---

Nodes:
- (:Actor:Person {name, born, died, bornIn, tmdbId, imdbId, url})
- (:Director:Person {name, born, died, bornIn, bio, tmdbId, imdbId, url})
- (:Movie {title, year, imdbRating, imdbVotes, imdbId, tmdbId, runtime, countries, languages, revenue, budget, plot, poster, url, released})
- (:Genre {name})
- (:User {name, userId})
- (:Session {id})
- (:Message {type, content, timestamp})

Relationships:
- (a:Actor)-[:ACTED_IN {role}]->(m:Movie)
- (d:Director)-[:DIRECTED]->(m:Movie)
- (m:Movie)-[:IN_GENRE]->(g:Genre)
- (u:User)-[:RATED {rating, timestamp}]->(m:Movie)
- (s:Session)-[:LAST_MESSAGE]->(msg:Message)
- (msg1:Message)-[:NEXT]->(msg2:Message)

--- SAMPLE DATA ---

(:Actor:Person {name: "François Lallement", born: "1877-02-04", died: "1954-01-01", bornIn: "France", tmdbId: "1271225", imdbId: "2083046", url: "https://themoviedb.org/person/1271225"})

(:Director:Person {name: "Harold Lloyd", born: "1893-04-20", died: "1971-03-08", bornIn: "Burchard, Nebraska, USA", bio: "Famous silent film comedian...", tmdbId: "88953", imdbId: "0516001", url: "https://themoviedb.org/person/88953"})

(:Movie {title: "Toy Story", year: 1995, imdbRating: 8.3, imdbVotes: 591836, imdbId: "0114709", tmdbId: "862", runtime: 81, countries: ["USA"], languages: ["English"], revenue: 373554033, budget: 30000000, plot: "A cowboy doll is threatened when a new spaceman figure supplants him.", poster: "https://image.tmdb.org/t/p/w440_and_h660_face/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg", url: "https://themoviedb.org/movie/862", released: "1995-11-22"})

(:Genre {name: "Adventure"})

(:User {name: "Omar Huffman", userId: "1"})

Relationships:
- (Actor: "François Lallement")-[:ACTED_IN {role: "Officer of the Marines (uncredited)"}]->(Movie: "Trip to the Moon, A")
- (Director: "Harold Lloyd")-[:DIRECTED]->(Movie: "Kid Brother, The")
- (Movie: "Toy Story")-[:IN_GENRE]->(Genre: "Adventure")
- (User: "Omar Huffman")-[:RATED {rating: 2.0, timestamp: 1260759108}]->(Movie: "Antz")
- (Session {id: "d7ff64c7-b0f8-436f-934e-8e6201342a83"})-[:LAST_MESSAGE]->(Message {type: "ai", content: "The CEO of Google is Sundar Pichai."})
- (Message {type: "human", content: "WHO IS THE CEO OF GOOGLE?"})-[:NEXT]->(Message {type: "ai", content: "The CEO of Google is Sundar Pichai."})
"""


def call_openai_chat(messages, model=MODEL_CHAT, temperature=0.0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


def generate_cypher(user_question):
    prompt = f"""
{SCHEMA_AND_SAMPLES}

Using the above schema and sample data, generate a valid Cypher query ONLY for the following request.
Make sure to filter out or ignore any null or missing values in the results.

Question: {user_question}

Cypher query:
"""
    messages = [
        {"role": "system", "content": "You are an expert Cypher generator."},
        {"role": "user", "content": prompt},
    ]
    response = client.chat.completions.create(
        model=MODEL_CYPHER,
        messages=messages,
        temperature=0.0,
        max_tokens=150,
    )
    cypher = response.choices[0].message.content.strip()
    return cypher
