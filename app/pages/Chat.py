import streamlit as st

from rentradar.llm.agent import RentRadarLLMAgent


def initialize_sidebar():
    """Set up the sidebar with API key input and relevant links."""
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key", key="chatbot_api_key", type="password"
    )
    st.sidebar.markdown(
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    )
    return openai_api_key


def display_messages():
    """Display messages from the chat history."""
    for message in st.session_state["messages"]:
        if message.startswith("Assistant:"):
            st.info(message)
        elif message.startswith("User:"):
            st.success(message)


def append_and_display_message(role, content):
    """Append a message to the chat history and display it."""
    message = f"{role}: {content}"
    st.session_state["messages"].append(message)
    if role == "Assistant":
        st.info(message)
    else:
        st.success(message)


def handle_user_input(openai_api_key):
    """Process the user input using the chatbot agent."""
    user_input = st.text_input("Type your question here:")
    if st.button("Send") and user_input:
        if not openai_api_key:
            st.error("Please add your OpenAI API key to continue.")
            st.stop()

        append_and_display_message("User", user_input)
        agent = RentRadarLLMAgent(
            db_uri="duckdb:///rentradar/db/rentradar.db", openai_api_key=openai_api_key
        )

        try:
            response = agent.execute_query(user_input)
            response_message = response
        except Exception as e:
            response_message = "Sorry, I encountered an error processing your query."
            st.exception(e)

        append_and_display_message("Assistant", response_message)
        st.rerun()


def run_chatbot():
    """Main function to run the RentRadar Chatbot."""
    st.title("💬 RentRadar Chatbot")
    st.caption("🚀 A RentRadar chatbot powered by OpenAI & LangChain")

    openai_api_key = initialize_sidebar()

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            "Assistant: Hello! How can I assist you with real estate data today?"
        ]

    display_messages()
    handle_user_input(openai_api_key)


if __name__ == "__main__":
    run_chatbot()
