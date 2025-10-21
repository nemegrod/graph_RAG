# Graph RAG Architecture

## Overview

This document describes the architecture of the **Graph RAG (Retrieval-Augmented Generation)** application that combines **OpenAI GPT** with **GraphDB knowledge graphs** for intelligent jaguar conservation queries. The application demonstrates how to build a conversational AI that can query structured data using SPARQL and provide natural language responses.

## Graph RAG High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Flask Web Application                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Single-File POC                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │   Routes    │  │ Templates   │  │   Global    │ │   │
│  │  │  - /chat    │  │  - index.html│  │   State     │ │   │
│  │  │  - /clear   │  │  - Chat UI  │  │  - AGENT    │ │   │
│  │  │  - /        │  │  - Error    │  │  - THREAD   │ │   │
│  │  └─────────────┘  └─────────────┘  │  - HISTORY  │ │   │
│  │                                    └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                Microsoft Agent Framework                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            Jaguar Conservation Agent                 │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │            System Prompt                    │   │   │
│  │  │  - Graph RAG Instructions                   │   │   │
│  │  │  - SPARQL Guidelines                        │   │   │
│  │  │  - Response Formatting                      │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  │                                                   │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │            OpenAI Client                    │   │   │
│  │  │  - GPT-4 Integration                       │   │   │
│  │  │  - Function Calling                        │   │   │
│  │  │  - Thread Management                       │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  │                                                   │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │            GraphDB Tool                     │   │   │
│  │  │  - SPARQL Query Execution                   │   │   │
│  │  │  - Query Validation                        │   │   │
│  │  │  - Result Processing                       │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    External Systems                         │
│  ┌─────────────────┐              ┌─────────────────────┐   │
│  │   OpenAI API    │              │      GraphDB        │   │
│  │  - GPT-4        │              │  - RDF Triple Store │   │
│  │  - Responses    │              │  - SPARQL Engine    │   │
│  │  - Function     │              │  - Jaguar Ontology  │   │
│  │    Calling      │              │  - Conservation     │   │
│  └─────────────────┘              │    Data             │   │
│                                   └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Graph RAG Component Descriptions

### Flask Web Application (Single-File POC)
- **Routes**: Simple Flask routes (`/`, `/chat`, `/clear`)
- **Templates**: HTML template with chat interface
- **Global State**: In-memory storage for single-user POC
  - `app.config['AGENT']`: Single agent instance
  - `app.config['THREAD']`: Single conversation thread
  - `app.config['CHAT_HISTORY']`: UI display history
  - `app.config['ERROR']`: Error display

### Microsoft Agent Framework
- **Jaguar Conservation Agent**: Graph RAG specialist agent
- **System Prompt**: Graph RAG instructions and SPARQL guidelines
- **OpenAI Client**: GPT-4 integration with function calling
- **Thread Management**: Conversation context preservation

### Graph RAG Tools
- **GraphDB Tool**: Core Graph RAG component
  - Executes SPARQL queries against knowledge graph
  - Validates query syntax and ontology compliance
  - Processes and formats query results

### External Systems
- **OpenAI API**: GPT-4 model for natural language processing
- **GraphDB**: RDF triple store with jaguar conservation ontology

## Graph RAG Data Flow

### User Query Processing

1. **User Request**: User sends message via web interface
2. **Flask Route**: `/chat` route receives POST request
3. **Agent Retrieval**: Get singleton agent and thread instances
4. **Graph RAG Processing**:
   - **LLM Analysis**: OpenAI GPT analyzes natural language query
   - **SPARQL Generation**: AI generates appropriate SPARQL query
   - **Tool Call Detection**: Agent Framework detects need for GraphDB tool
5. **Knowledge Graph Query**:
   - **SPARQL Execution**: `query_jaguar_database` tool executes query
   - **Result Processing**: Raw SPARQL results processed and formatted
6. **Response Generation**:
   - **LLM Interpretation**: OpenAI GPT interprets GraphDB results
   - **Natural Language Response**: Generates human-readable response
   - **Markdown Formatting**: Applies formatting with code blocks
7. **State Update**:
   - **Thread Persistence**: Agent Framework maintains conversation context
   - **UI History**: Flask app stores display history
   - **Response Delivery**: Return formatted response to user

## Graph RAG Design Patterns

### 1. Singleton Pattern
Single-user POC uses singleton pattern for global access:
```python
def get_agent():
    """Get or create the jaguar agent (singleton)"""
    if app.config['AGENT'] is None:
        app.config['AGENT'] = create_jaguar_agent()
    return app.config['AGENT']
```

### 2. Agent Framework Pattern
Microsoft Agent Framework handles conversation management:
```python
# Agent Framework manages threads and context
response = asyncio.run(agent.run(user_message, thread=thread, store=True))
```

### 3. Graph RAG Pattern
Combines LLM with knowledge graph queries:
```python
# LLM generates SPARQL, tool executes against GraphDB
tools=[query_jaguar_database]
tool_choice="auto"
```

## Graph RAG State Management

### Simplified POC State
```python
# Global Flask app configuration for single-user POC
app.config['AGENT'] = None        # Single agent instance
app.config['THREAD'] = None       # Single conversation thread  
app.config['CHAT_HISTORY'] = []   # UI display history
app.config['ERROR'] = None        # Error display
```

### Thread Management
- **Agent Framework**: Microsoft Agent Framework manages conversation context
- **OpenAI Responses API**: Server-side thread persistence
- **Flask App**: Simple UI state management

## Graph RAG Configuration

### Environment Variables
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_RESPONSES_MODEL_ID=gpt-4

# GraphDB Configuration
GRAPHDB_URL=http://localhost:7200
GRAPHDB_REPOSITORY=jaguar_conservation
```

### Agent Settings
```python
# Hardcoded in create_jaguar_agent() function
settings = OpenAISettings(
    api_key=os.getenv("OPENAI_API_KEY", ""),
    model_id=os.getenv("OPENAI_RESPONSES_MODEL_ID", "gpt-4")
)
```

## Graph RAG Security

### API Security
1. **API Keys**: Stored in `.env`, never committed to repository
2. **Input Validation**: User inputs validated before processing
3. **Error Handling**: Errors logged but sanitized for user display
4. **SPARQL Injection Prevention**: Tool validates SPARQL syntax

### Data Privacy
- **Read-Only Access**: Agent only reads from GraphDB
- **No Data Storage**: No user data persisted beyond conversation
- **Secure APIs**: Use HTTPS for all external communications

## Graph RAG Scalability

### Current POC State
- Single-file Flask application
- In-memory state storage
- Single-user design
- OpenAI API rate limits

### Future Enhancements
1. **Multi-User Support**: Session-based user management
2. **Distributed State**: Redis or database backend
3. **Horizontal Scaling**: Multiple Flask instances
4. **Query Caching**: Cache frequent SPARQL patterns
5. **Async Processing**: Non-blocking GraphDB queries

## Graph RAG Monitoring

### Logging
- Flask request/response logging
- Agent Framework conversation logging
- GraphDB query execution logging

### Performance Metrics
- **Response Times**: Graph RAG query processing time
- **Query Success Rate**: SPARQL execution success rate
- **Tool Usage**: GraphDB tool call frequency

## Graph RAG Testing

### Manual Testing
1. **Web Interface**: Test queries through Flask UI
2. **SPARQL Validation**: Verify generated queries in GraphDB
3. **Response Quality**: Check natural language response accuracy

### Example Test Queries
```python
# Test basic counting
"How many jaguars are in the database?"

# Test filtering
"Show me all male jaguars"

# Test relationships
"Which jaguars were rescued and by which organization?"
```

## Graph RAG Dependencies

### Core Dependencies
- **Flask 3.0.0**: Web framework
- **OpenAI 1.51.0**: GPT API client
- **Microsoft Agent Framework**: Agent management
- **Requests**: GraphDB HTTP communication

### Graph RAG Specific
- **GraphDB**: RDF triple store
- **SPARQL**: Query language for knowledge graphs
- **RDF/Turtle**: Ontology format

## Graph RAG Project Structure

```
graph_RAG/
├── app.py                    # Single-file Flask application
├── templates/
│   └── index.html           # Chat interface template
├── src/
│   ├── agents/
│   │   └── jaguar_agent.py  # Agent creation (deprecated)
│   └── tools/
│       └── query_jaguar_database.py  # GraphDB tool with inline logic
├── docs/
│   ├── agent_design.md      # Agent design documentation
│   └── architecture.md      # Architecture documentation
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## Graph RAG Benefits

### Technical Benefits
- **Hybrid Intelligence**: Combines LLM reasoning with structured data
- **Real-time Queries**: Live data from knowledge graphs
- **Context Awareness**: Maintains conversation context
- **Extensible**: Easy to add new tools and capabilities

### Conservation Benefits
- **Data-Driven Insights**: Access to structured conservation data
- **Natural Language Interface**: Easy querying of complex data
- **Educational Tool**: Demonstrates Graph RAG capabilities
- **Research Support**: Facilitates conservation research queries

