import os
import json
from openai import AzureOpenAI
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from dotenv import load_dotenv
from graph_rag_tool import GraphDBTool

from models import ChatHistory, Message

# Load environment variables
load_dotenv()

class LLMService:
    def __init__(self):
        self.client = AzureOpenAI(
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_ad_token_provider=None,
        )
        self.model_deployment_name = os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT")
        self.graphdb_tool = GraphDBTool(
            graphdb_url=os.getenv("GRAPHDB_URL", "http://localhost:7200"),
            repository=os.getenv("GRAPHDB_REPOSITORY", "Jaguars")
        )
        
        # Get the tool definition from the GraphDB tool
        self.tools = [self.graphdb_tool.get_tool_definition()]

    def get_chat_response(self, chat_history: ChatHistory, user_message: str) -> str:
        """
        Get a response from the LLM based on chat history and new user message
        Includes Graph RAG capabilities for jaguar-related queries
        """
        try:
            # Add the new user message to history
            chat_history.add_message("user", user_message)
            
            # Prepare messages for API call
            messages = [
                {
                    "role": "system",
                    "content": """You are a helpful assistant with access to a comprehensive jaguar database stored in GraphDB. 
                    When users ask questions about jaguars, jaguar populations, conservation efforts, habitats, 
                    threats, or any jaguar-related information, use the query_jaguar_database function with a valid SPARQL query.
                    Always try to use the function to get accurate data from the database.
                    When using the function: 
                        - Make sure to from a simple query and only add complexity if needed.
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
                    - Always mention that the information comes from the jaguar database""",
                }
            ]
            
            # Add chat history to messages
            messages.extend(chat_history.get_messages_for_api())
            
            # Make initial API call with function calling capability
            response = self.client.chat.completions.create(
                model=self.model_deployment_name,
                messages=messages,
                max_completion_tokens=30000,
                reasoning_effort="low",
                tools=self.tools,
                tool_choice="auto"
            )
            
            # Process the response
            assistant_message = response.choices[0].message
            
            # Check if the LLM wants to call a function
            if assistant_message.tool_calls:
                # Execute function calls
                for tool_call in assistant_message.tool_calls:
                    if tool_call.function.name == "query_jaguar_database":
                        # Parse the function arguments
                        function_args = json.loads(tool_call.function.arguments)
                        sparql_query = function_args.get("sparql_query", "")
                        
                        # Execute the SPARQL query and get JSON results
                        query_result_json = self.graphdb_tool.execute_sparql_json(sparql_query)
                        
                        # Convert JSON result to string for LLM to interpret
                        query_result = json.dumps(query_result_json, indent=2)
                        
                        # Add the function call and result to the message history
                        messages.append({
                            "role": "assistant",
                            "content": None,
                            "tool_calls": [
                                {
                                    "id": tool_call.id,
                                    "type": "function",
                                    "function": {
                                        "name": "query_jaguar_database",
                                        "arguments": tool_call.function.arguments
                                    }
                                }
                            ]
                        })
                        
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": query_result
                        })
                
                # Make a second API call to get the final response
                final_response = self.client.chat.completions.create(
                    model=self.model_deployment_name,
                    messages=messages,
                    max_completion_tokens=30000,
                    reasoning_effort="medium"
                )
                
                assistant_response = final_response.choices[0].message.content
            else:
                # No function call needed, use the direct response
                assistant_response = assistant_message.content
            
            # Post-process the response for better formatting
            assistant_response = self.format_response(assistant_response)
            
            # Add assistant response to history
            chat_history.add_message("assistant", assistant_response)
            
            return assistant_response
            
        except Exception as e:
            error_message = f"Error communicating with LLM: {str(e)}"
            chat_history.add_message("assistant", error_message)
            return error_message

    def format_response(self, response: str) -> str:
        """
        Post-process the LLM response for better formatting
        """
        if not response:
            return response
            
        # Ensure proper paragraph breaks
        response = response.replace('. ', '.\n\n')
        
        # Fix multiple consecutive line breaks
        while '\n\n\n' in response:
            response = response.replace('\n\n\n', '\n\n')
        
        # Clean up and format the response
        lines = response.split('\n')
        formatted_lines = []
        
        for line in lines:
            stripped_line = line.strip()
            if stripped_line:
                formatted_lines.append(stripped_line)
            elif formatted_lines and formatted_lines[-1]:  # Only add empty line if previous line wasn't empty
                formatted_lines.append('')
        
        return '\n'.join(formatted_lines)
