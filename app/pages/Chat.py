import streamlit as st

from rentradar.llm.agent import RentRadarLLMAgent


def main():
    st.title("🦜🔗 RentRadar LLM Agent")
    st.sidebar.markdown("# 🦜🔗 LLM Config")

    # Securely request the API key
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

    if openai_api_key:
        # Initialize the agent with the provided API key and database URI
        agent = RentRadarLLMAgent(
            db_uri="duckdb:///rentradar/db/rentradar.db", openai_api_key=openai_api_key
        )

        st.markdown("## Ask me about real estate market data!")
        user_input = st.text_input("Type your question here and press enter:")

        if user_input:
            try:
                response = agent.execute_query(user_input)
                st.write("Response:")
                st.success(response)
            except Exception as e:
                st.error("Error processing your query:")
                st.exception(e)
    else:
        st.warning("Please enter your OpenAI API key to enable the agent.")


if __name__ == "__main__":
    main()
