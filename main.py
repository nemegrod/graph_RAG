import asyncio
import os
from dotenv import load_dotenv
from agent_framework.openai import OpenAIResponsesClient, OpenAISettings
from agent_framework import ChatAgent
from agent_framework.devui import serve
from src.agents.jaguar_agent import create_jaguar_agent

def main():
    """Start the dev UI"""
    agent = create_jaguar_agent()
    
    # Create DevUI instance
    serve(entities=[agent], auto_open=True)

if __name__ == "__main__":
    main()