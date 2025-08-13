import streamlit as st
from agent import ChatAgent
from bot import chatbot_answer

st.set_page_config(page_title="Neo4j-backed Movie Chatbot")
st.title("🎬 Neo4j-backed Chatbot")

if "agent" not in st.session_state:
    st.session_state.agent = ChatAgent()

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Ask about movies, actors, genres, or recommendations:")

if st.button("Ask") or user_input.strip():
    agent = st.session_state.agent

    # Store user message in graph
    agent.add_user_message(user_input)
    st.session_state.history.append({"role": "user", "text": user_input})

    answer, cypher = chatbot_answer(user_input)

    if cypher:
        st.write("**Generated Cypher:**")
        st.code(cypher, language="cypher")

    st.write("**Answer:**")
    st.write(answer)

    # Store bot answer in graph
    agent.add_bot_message(answer)
    st.session_state.history.append({"role": "assistant", "text": answer})

# Show conversation history
st.markdown("---")
st.write("### Conversation history")
for item in st.session_state.history[-10:]:
    if item["role"] == "user":
        st.markdown(f"**You:** {item['text']}")
    else:
        st.markdown(f"**Bot:** {item['text']}")
