from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

from rentradar.llm.templates import rr_template


class RentRadarLLMAgent:
    def __init__(self, db_uri: str):
        """
        Initializes the RentRadar LLM Agent with connection to the DuckDB database.

        Parameters:
            db_uri (str): URI to connect to the DuckDB database.
        """
        self.db = SQLDatabase.from_uri(db_uri, sample_rows_in_table_info=3)
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=OpenAI(temperature=0))
        self.agent_executor = create_sql_agent(
            llm=OpenAI(temperature=0),
            toolkit=self.toolkit,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
        self.prompt_template = PromptTemplate.from_template(rr_template)

    def execute_query(self, query):
        """
        Executes a given SQL query using the LLM agent and returns the result.

        Parameters:
            query (str): The SQL query to be executed by the LLM agent.

        Returns:
            The result of the executed query.
        """
        formatted_prompt = self.prompt_template.format(query=query)
        result = self.agent_executor.invoke(formatted_prompt)
        return result
