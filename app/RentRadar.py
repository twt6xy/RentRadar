import streamlit as st

from rentradar.db.duckdb import DuckDBManager


def main():
    st.set_page_config(page_title="RentRadar", layout="wide")

    st.markdown(
        """
        <div style='text-align: center;'>
            <h1>Welcome to RentRadar 🏘️</h1>
            <p>A Data Platform for Real Estate Market Analysis</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        RentRadar is a data platform designed to streamline real estate market analysis. It offers a range of modules for data ingestion, database management, and API access to real estate data, empowering users to make informed decisions in the dynamic world of real estate.

        With RentRadar, you can:
        - Explore and analyze market trends and insights
        - Access data through a user-friendly API
        """
    )

    st.markdown(
        """
        ## Property Coverage

        RentRadar currently has comprehensive data for all properties in **Charlottesville, Virginia** in its database. We can add more cities upon request.
        """
    )

    st.markdown("## Database Schema")

    with DuckDBManager("rentradar/db/rentradar.db") as db_manager:
        schema_df = db_manager.get_database_schema()

    st.dataframe(schema_df, height=300, use_container_width=True)

    st.markdown("## Explore RentRadar")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <h3><a href="/Charts" target="_self">📊 Charts</a></h3>

            Dive into interactive charts and visualizations to uncover patterns and trends in the real estate market. Build custom charts using our intuitive Chart Builder.
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <h3><a href="/Map" target="_self">🗺️ Map</a> (Coming Soon)</h3>

            Visualize real estate data on an interactive map. Explore properties, prices, and market dynamics across different geographical regions.
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <h3><a href="/Chat" target="_self">💬 Chat</a> (Coming Soon)</h3>

            Engage in interactive conversations with our AI-powered chat assistant. Get instant answers to your real estate questions and receive personalized recommendations.
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        ## GitHub

        Explore the source code, contribute to the project, and learn more about RentRadar on our GitHub repository:

        <div style='text-align: center;'>
            <a href='https://github.com/twt6xy/RentRadar' target='_blank'>
                <img src='https://img.shields.io/badge/GitHub-RentRadar-blue?style=flat&logo=github' alt='RentRadar GitHub Repository'>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
