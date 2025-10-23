"""
DEPRECATED: Jaguar Conservation Agent - Using Microsoft Agent Framework

This file has been deprecated. The agent code has been moved directly into app.py
for the single-user POC. This file is kept for reference only.

The agent creation logic is now in app.py as create_jaguar_agent().
"""
import os
from dotenv import load_dotenv
from agent_framework.openai import OpenAIResponsesClient, OpenAISettings
from agent_framework import ChatAgent
from src.agents.jaguar_tool import query_jaguar_database

# Load environment variables
load_dotenv()


def create_jaguar_query_agent():
    """
    Create and return a native Agent Framework agent for jaguar conservation.
    
    Returns:
        Agent Framework ChatAgent instance
    """
    # System prompt for the agent
    system_prompt = """You are a helpful assistant with access to a comprehensive jaguar database stored in GraphDB. 
When users ask questions about jaguars, jaguar populations, conservation efforts, habitats, threats, or any jaguar-related information, 
use the query_jaguar_database function with a valid SPARQL query. Always try to use the function to get accurate data from the database.

When using the function:
- Make sure to form a simple query and only add complexity if needed.
- Make sure your queries are based on the provided jaguar ontology. Don't make up properties or classes not in the ontology.
- Answer based on the data retrieved, never your training data.

When responding:
- Show the used SPARQL one time and one time only
- Formulate a readable answer based on the query results
- Use **bold** for emphasis when appropriate
- Use bullet points or numbered lists for multiple items
- Use code blocks with ``` for SPARQL queries when showing them
- Break up long responses into paragraphs
- Be concise but comprehensive in your answers
- Always mention that the information comes from the jaguar database"""
    
        # OpenAI settings
    settings = OpenAISettings(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        model_id=os.getenv("OPENAI_RESPONSES_MODEL_ID", "gpt-4")
    )
    
    # Create client
    client = OpenAIResponsesClient(settings=settings)
    
    # Create and return native Agent Framework agent
    agent = ChatAgent(
        client,
        name="JaguarQueryAgent",
        instructions=system_prompt,
        tools=[query_jaguar_database],
        tool_choice="auto"
    )
    
    return agent

