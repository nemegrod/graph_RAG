# Jaguar Conservation Agent Design

## Overview

The Jaguar Conservation Agent is an AI agent specialized in querying and providing information about jaguar conservation from a GraphDB knowledge base. This document describes the agent's design, capabilities, and usage patterns.

## Agent Characteristics

### Identity
- **Name**: JaguarConservationAgent
- **Role**: Conservation information specialist
- **Domain**: Jaguar population, conservation, habitats, threats

### Capabilities
1. Query jaguar-related data from GraphDB using SPARQL
2. Interpret complex ontology structures
3. Provide natural language responses
4. Maintain conversation context
5. Format responses with markdown

## Architecture

### Components

```
┌─────────────────────────────────────────┐
│        Jaguar Agent                      │
│  ┌───────────────────────────────┐      │
│  │      Configuration            │      │
│  │  - System Prompt              │      │
│  │  - Model Parameters           │      │
│  │  - Middleware Settings        │      │
│  └───────────────────────────────┘      │
│                                          │
│  ┌───────────────────────────────┐      │
│  │      Middleware Stack         │      │
│  │  - Logging Middleware         │      │
│  │  - Telemetry Middleware       │      │
│  └───────────────────────────────┘      │
│                                          │
│  ┌───────────────────────────────┐      │
│  │      LLM Client               │      │
│  │  - Azure OpenAI Integration   │      │
│  │  - Function Calling           │      │
│  └───────────────────────────────┘      │
│                                          │
│  ┌───────────────────────────────┐      │
│  │      Tool Registry            │      │
│  │  - GraphDB Tool               │      │
│  │  - (Future tools)             │      │
│  └───────────────────────────────┘      │
│                                          │
│  ┌───────────────────────────────┐      │
│  │    Thread Manager             │      │
│  │  - Session State              │      │
│  │  - Chat History               │      │
│  └───────────────────────────────┘      │
└─────────────────────────────────────────┘
```

## System Prompt

The agent uses a carefully crafted system prompt that:
1. Defines its role and capabilities
2. Provides ontology context
3. Sets response formatting guidelines
4. Establishes query generation rules

Key instructions:
- Use GraphDB tool for jaguar-related queries
- Form simple queries first, add complexity only if needed
- Base queries on provided ontology
- Show SPARQL query once
- Use markdown formatting
- Mention data source in responses

## Tool Integration

### GraphDB Tool

The agent's primary tool for data retrieval:

**Function Name**: `query_jaguar_database`

**Parameters**:
- `sparql_query`: SPARQL query string

**Ontology Coverage**:
- Classes: Jaguar, Habitat, Location, Threat, ConservationEffort, etc.
- Properties: hasGender, wasKilled, rescuedBy, facesThreat, etc.

**Query Examples**:
```sparql
# Count jaguars
SELECT (COUNT(?jaguar) as ?count) WHERE { 
  ?jaguar a :Jaguar . 
}

# Find by gender
SELECT ?jaguar ?label ?gender WHERE { 
  ?jaguar a :Jaguar . 
  OPTIONAL { ?jaguar rdfs:label ?label . } 
  OPTIONAL { ?jaguar :hasGender ?gender . } 
}

# Find killed jaguars
SELECT ?jaguar ?label ?causeOfDeath WHERE { 
  ?jaguar a :Jaguar . 
  ?jaguar :wasKilled true . 
  OPTIONAL { ?jaguar rdfs:label ?label . } 
  OPTIONAL { ?jaguar :causeOfDeath ?causeOfDeath . } 
}
```

## Message Processing Flow

### 1. Receive Message
```python
agent.process_message(session_id, user_message)
```

### 2. Before Request Middleware
- Log the incoming message
- Record telemetry

### 3. Context Retrieval
- Get or create thread for session
- Load chat history
- Add user message to history

### 4. LLM Processing
- Prepare messages (system + history)
- Call Azure OpenAI with tools
- Check for tool calls

### 5. Tool Execution (if needed)
- Parse tool call arguments
- Log tool invocation
- Execute SPARQL query
- Log tool result
- Handle errors

### 6. Final Response
- Send tool results back to LLM
- Generate natural language response
- Format response (paragraphs, markdown)

### 7. After Response Middleware
- Log the response
- Record telemetry

### 8. State Update
- Add assistant message to history
- Update thread metadata
- Return response

## Middleware

### Logging Middleware

Logs all agent interactions:
- User requests
- Tool calls
- Tool results
- Assistant responses
- Errors

**Configuration**:
```json
{
  "logging": {
    "enabled": true,
    "log_level": "INFO"
  }
}
```

### Telemetry Middleware (Placeholder)

Collects metrics:
- Request count
- Tool call count
- Error count
- Response times (future)

**Configuration**:
```json
{
  "telemetry": {
    "enabled": false
  }
}
```

## State Management

### Thread Structure
```python
{
  "state": AgentState(
    session_id="...",
    thread_id=None,
    metadata={}
  ),
  "chat_history": ChatHistory(),
  "created_at": datetime,
  "last_accessed": datetime
}
```

### Chat History
- Stores all messages (user, assistant, tool)
- Maintains timestamps
- Supports retrieval (all or last N)
- Can be cleared

### Context
```python
AgentContext(
  session_id="...",
  user_id=None,
  conversation_metadata={},
  environment={}
)
```

## Configuration

### Model Configuration
```json
{
  "max_completion_tokens": 30000,
  "reasoning_effort": "low",
  "tool_choice": "auto"
}
```

### Reasoning Configuration
```json
{
  "final_response_reasoning_effort": "medium"
}
```

## Response Formatting

The agent applies post-processing to responses:
1. Add paragraph breaks after sentences
2. Remove excessive line breaks
3. Strip whitespace
4. Preserve markdown formatting

## Error Handling

### Levels of Error Handling

1. **Tool Level**: GraphDB connection errors, query syntax errors
2. **Agent Level**: LLM API errors, processing errors
3. **Middleware Level**: Logging errors don't stop execution
4. **Web Level**: HTTP errors, validation errors

### Error Response Format
```json
{
  "error": "Error message",
  "success": false
}
```

## Usage Examples

### Basic Usage
```python
from src.agents.jaguar_agent import get_jaguar_agent

agent = get_jaguar_agent()
response = agent.process_message("session123", "How many jaguars are in the database?")
print(response)
```

### Clear History
```python
agent.clear_history("session123")
```

### Get History
```python
history = agent.get_history("session123")
for msg in history:
    print(f"{msg['role']}: {msg['content']}")
```

### Agent Info
```python
info = agent.get_agent_info()
print(f"Agent: {info['name']}")
print(f"Tools: {info['tools']}")
print(f"Active sessions: {info['active_sessions']}")
```

## Future Enhancements

### Multi-Agent Capabilities
1. **Research Agent**: Deep dive into specific topics
2. **Visualization Agent**: Create charts and graphs
3. **Conservation Agent**: Provide recommendations

### Advanced Features
1. **Streaming Responses**: Real-time response generation
2. **Async Processing**: Non-blocking tool execution
3. **Checkpointing**: Save/restore conversation state
4. **Human-in-the-Loop**: Request user clarification
5. **Memory Management**: Summarize old conversations

### Additional Tools
1. **Web Search**: Find recent conservation news
2. **Document Analysis**: Parse PDF reports
3. **Image Analysis**: Analyze jaguar photos
4. **Data Export**: Export query results

## Testing

### Unit Tests
```python
# Test agent initialization
def test_agent_init():
    agent = JaguarAgent()
    assert agent.config.name == "JaguarConservationAgent"

# Test message processing (mocked)
def test_process_message():
    agent = JaguarAgent()
    # Mock LLM and tools
    response = agent.process_message("test", "Test message")
    assert response is not None
```

### Integration Tests
```python
# Test with real GraphDB (test instance)
def test_agent_with_graphdb():
    agent = get_jaguar_agent()
    response = agent.process_message(
        "test",
        "Count the jaguars"
    )
    assert "jaguar" in response.lower()
```

## Performance Considerations

### Response Time
- Average: 2-5 seconds (with tool call)
- No tool call: 1-2 seconds
- Complex queries: 5-10 seconds

### Optimization Strategies
1. Cache frequent SPARQL queries
2. Limit conversation history context
3. Use async for tool execution
4. Implement response streaming

### Resource Usage
- Memory: ~100MB per session
- CPU: Minimal (I/O bound)
- Network: Dependent on LLM/GraphDB latency

## Security

### Input Validation
- Validate session IDs
- Sanitize user messages
- Limit message length

### SPARQL Injection Prevention
- Tool validates SPARQL syntax
- GraphDB handles query validation
- Error messages sanitized

### Access Control
- Session-based isolation
- No cross-session data access
- Future: User authentication/authorization

