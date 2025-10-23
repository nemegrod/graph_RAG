import asyncio
import os
from dotenv import load_dotenv
from agent_framework.openai import OpenAIResponsesClient, OpenAISettings
from agent_framework import ChatAgent
from agent_framework.devui import serve
from src.agents.jaguar_query_agent import create_jaguar_query_agent

def main():
    """Start the dev UI"""
    query_agent = create_jaguar_query_agent()
    
    # Create DevUI instance
    serve(entities=[query_agent], auto_open=True)

if __name__ == "__main__":
    main()