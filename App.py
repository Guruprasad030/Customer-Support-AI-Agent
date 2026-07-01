#App. Py#
import streamlit as st
from chatbot import CustomerSupportBot
from database import TicketDatabase

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="Customer Support AI Agent",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------
# Initialize Bot & Database
# ---------------------------
bot = CustomerSupportBot()
db = TicketDatabase()

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("🤖 Customer Support AI")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Chat Assistant",
        "Raise Ticket",
        "View Tickets",
        "About"
    ]
)

# ---------------------------
# Chat Assistant
# ---------------------------
if menu == "Chat Assistant":

    st.title("💬 AI Customer Support")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask your question...")

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        answer = bot.ask(question)

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

# ---------------------------
# Raise Ticket
# ---------------------------
elif menu == "Raise Ticket":

    st.title("🎫 Raise Support Ticket")

    name = st.text_input("Name")

    email = st.text_input("Email")

    issue = st.text_area("Describe your issue")

    priority = st.selectbox(
        "Priority",
        [
            "Low",
            "Medium",
            "High",
            "Critical"
        ]
    )

    if st.button("Submit Ticket"):

        db.add_ticket(
            name=name,
            email=email,
            issue=issue,
            priority=priority
        )

        st.success("Ticket submitted successfully!")

# ---------------------------
# View Tickets
# ---------------------------
elif menu == "View Tickets":

    st.title("📋 Support Tickets")

    tickets = db.get_all_tickets()

    if len(tickets) == 0:
        st.info("No tickets available.")

    else:

        for ticket in tickets:

            with st.expander(
                f"Ticket #{ticket['id']} - {ticket['priority']}"
            ):

                st.write("**Name:**", ticket["name"])
                st.write("**Email:**", ticket["email"])
                st.write("**Issue:**", ticket["issue"])
                st.write("**Status:**", ticket["status"])

# ---------------------------
# About
# ---------------------------
elif menu == "About":

    st.title("ℹ️ About")

    st.write("""
This Customer Support AI Agent provides:

- 🤖 AI Chatbot
- 📄 FAQ Search
- 🎫 Ticket Management
- 🧠 Conversation Memory
- 📊 SQLite Database
- ⚡ Streamlit Interface
- 🔍 RAG-based Knowledge Retrieval
""")
