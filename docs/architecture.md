# Graph RAG Architecture

## Overview

This document describes the architecture of the Graph RAG application after migration to the Microsoft Agent Framework patterns.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Layer (Flask)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Routes     │  │  Templates   │  │   Static     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                     Agent Layer                              │
│  ┌──────────────────────────────────────────────────┐       │
│  │         Jaguar Conservation Agent                 │       │
│  │  ┌──────────────┐  ┌──────────────┐            │       │
│  │  │    Config    │  │  Middleware  │            │       │
│  │  └──────────────┘  └──────────────┘            │       │
│  └──────────────────────────────────────────────────┘       │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  Context & State Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │Thread Manager│  │Context Prov. │  │ Chat History │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                     Tools Layer                              │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ GraphDB Tool │  │Tool Registry │                        │
│  └──────────────┘  └──────────────┘                        │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   Services Layer                             │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │  LLM Client  │  │GraphDB Svc.  │                        │
│  └──────────────┘  └──────────────┘                        │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  External Systems                            │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │Azure OpenAI  │  │   GraphDB    │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## Component Descriptions

### Web Layer
- **Routes**: API endpoints for chat, history, health checks
- **Templates**: HTML templates for the UI
- **Static**: CSS, JavaScript, images

### Agent Layer
- **Jaguar Agent**: Main AI agent for jaguar conservation queries
- **Configuration**: Agent-specific settings from JSON
- **Middleware**: Logging, telemetry, and other cross-cutting concerns

### Context & State Layer
- **Thread Manager**: Manages conversation sessions with state
- **Context Provider**: Provides agent memory and context
- **Chat History**: Stores message history per session

### Tools Layer
- **GraphDB Tool**: Executes SPARQL queries against GraphDB
- **Tool Registry**: Central registry for all agent tools

### Services Layer
- **LLM Client**: Azure OpenAI client wrapper
- **GraphDB Service**: GraphDB connection and query service

### External Systems
- **Azure OpenAI**: GPT model for natural language processing
- **GraphDB**: RDF triple store with jaguar ontology

## Data Flow

### User Query Processing

1. **User Request**: User sends message via web interface
2. **Route Handler**: Flask route receives request
3. **Session Management**: Get or create session ID
4. **Agent Processing**:
   - Retrieve conversation context
   - Add user message to history
   - Generate response using LLM
   - Check for tool calls
5. **Tool Execution** (if needed):
   - Parse tool arguments
   - Execute GraphDB query
   - Return results to LLM
6. **Response Generation**:
   - LLM interprets tool results
   - Formats natural language response
   - Applies middleware (logging, etc.)
7. **Response Delivery**: Return formatted response to user

## Key Design Patterns

### 1. Singleton Pattern
Services, tools, and agents use singleton pattern for global access:
```python
def get_jaguar_agent() -> JaguarAgent:
    global _jaguar_agent
    if _jaguar_agent is None:
        _jaguar_agent = JaguarAgent()
    return _jaguar_agent
```

### 2. Factory Pattern
Flask application uses factory pattern:
```python
def create_app():
    app = Flask(__name__)
    # ... configuration
    return app
```

### 3. Middleware Pattern
Agent uses middleware stack for cross-cutting concerns:
```python
middleware.before_request(session_id, message)
# ... process request
middleware.after_response(session_id, response)
```

### 4. Registry Pattern
Tools are registered centrally for discovery:
```python
registry.register_tool(name, definition, function)
tool = registry.execute_tool(name, **kwargs)
```

## State Management

### Thread-Based Sessions
Each user session is managed as a thread:
- Unique session ID
- Persistent chat history
- Metadata for context
- Checkpoint capability (for future use)

### Context Providers
Provide agent memory and state:
- Session context
- Conversation metadata
- User information
- Environment variables

## Configuration Management

### Environment Variables (.env)
- API keys and secrets
- External service URLs
- Flask configuration

### Agent Configuration (JSON)
- Agent system prompts
- Model parameters
- Middleware settings
- Tool configurations

## Security Considerations

1. **API Keys**: Stored in `.env`, never committed
2. **Session Management**: Flask sessions with secret key
3. **Input Validation**: All user inputs validated
4. **Error Handling**: Errors logged but sanitized for user display
5. **SPARQL Injection**: Parameters properly escaped

## Scalability Considerations

### Current State (Single Server)
- In-memory session storage
- Single Flask process
- No load balancing

### Future Enhancements
1. **Distributed Sessions**: Redis or database backend
2. **Horizontal Scaling**: Multiple Flask instances
3. **Async Processing**: Celery for long-running tasks
4. **Caching**: Redis for frequently accessed data
5. **Message Queue**: RabbitMQ for async tool execution

## Monitoring & Observability

### Logging
- Structured logging with levels
- File and console outputs
- Per-module loggers

### Telemetry (Planned)
- Request/response metrics
- Tool execution times
- Error rates
- Session analytics

### Health Checks
- `/health` endpoint
- Agent status
- Active session count

## Testing Strategy

### Unit Tests
- Individual components tested in isolation
- Mock external dependencies
- Test business logic

### Integration Tests
- Test component interactions
- Use test GraphDB instance
- Mock Azure OpenAI

### End-to-End Tests
- Full user flow testing
- Real external services (dev environment)

## Dependencies

### Core
- Flask 3.0.0
- Pydantic 2.5.0
- Azure OpenAI 1.51.0
- Requests (for GraphDB)

### Agent Framework (Future)
- microsoft-agent-framework (when fully integrated)

## Migration Notes

This architecture represents the migration from a flat structure to a layered, modular architecture following Microsoft Agent Framework patterns. The current implementation is compatible with Agent Framework concepts while maintaining backward compatibility with the existing Flask application.

Key improvements:
- Better separation of concerns
- Modular, testable components
- Scalable architecture
- Enterprise-ready patterns

