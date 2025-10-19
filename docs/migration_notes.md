# Migration Notes: Agent Framework Refactoring

## Overview

This document describes the migration from the original flat structure to the new Agent Framework-compatible architecture.

## What Changed

### Project Structure

**Before:**
```
graph_RAG/
├── app.py
├── llm_service.py
├── graph_rag_tool.py
├── models.py
└── templates/
    └── index.html
```

**After:**
```
graph_RAG/
├── src/
│   ├── agents/
│   │   └── jaguar_agent/
│   ├── tools/
│   ├── services/
│   ├── models/
│   ├── context/
│   ├── web/
│   └── utils/
├── data/
├── config/
├── tests/
└── docs/
```

### File Mapping

| Old File | New Location | Changes |
|----------|--------------|---------|
| `app.py` | `src/web/app.py` | Refactored with factory pattern, routes separated |
| N/A | `src/web/routes.py` | Routes extracted from app.py |
| `llm_service.py` | `src/agents/jaguar_agent/jaguar_agent.py` | Refactored as agent class |
| `graph_rag_tool.py` | `src/tools/graphdb_tool.py` | Enhanced with registry pattern |
| `models.py` | `src/models/chat_models.py`, `agent_models.py`, `graph_models.py` | Split into specific domains |
| N/A | `src/services/llm_client.py` | Extracted LLM client logic |
| N/A | `src/services/graphdb_service.py` | Extracted GraphDB logic |
| N/A | `src/context/thread_manager.py` | Replaces session dict |
| `templates/` | `src/web/templates/` | Moved to web module |
| `*.ttl`, `*.txt` | `data/` | Organized by type |

## Code Changes

### 1. Agent Implementation

**Before (llm_service.py):**
```python
class LLMService:
    def __init__(self):
        self.client = AzureOpenAI(...)
        self.graphdb_tool = GraphDBTool()
    
    def get_chat_response(self, chat_history, user_message):
        # Direct processing
        ...
```

**After (jaguar_agent.py):**
```python
class JaguarAgent:
    def __init__(self):
        self.config = JaguarAgentConfig()
        self.llm_client = get_llm_client()
        self.tool_registry = get_tool_registry()
        self.middleware = MiddlewareStack()
    
    def process_message(self, session_id, user_message):
        # Middleware-wrapped processing
        self.middleware.before_request(...)
        ...
        self.middleware.after_response(...)
```

### 2. State Management

**Before (app.py):**
```python
chat_sessions = {}  # In-memory dict

@app.route('/chat')
def chat():
    session_id = session.get('session_id')
    chat_history = chat_sessions.get(session_id, ChatHistory())
    ...
```

**After (routes.py + thread_manager.py):**
```python
# routes.py
def chat():
    session_id = session.get('session_id')
    agent.process_message(session_id, user_message)

# thread_manager.py
class ThreadManager:
    def get_or_create_thread(self, session_id):
        # Robust thread management with metadata
        ...
```

### 3. Configuration

**Before:**
```python
# Hardcoded in files
self.client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    ...
)
```

**After:**
```python
# Centralized configuration
from src.utils.config import config

self.client = AzureOpenAI(
    api_key=config.azure_openai_api_key,
    ...
)

# Agent config from JSON
agent_config = config.get_agent_config("jaguar_agent")
```

### 4. Tool Management

**Before (llm_service.py):**
```python
self.tools = [self.graphdb_tool.get_tool_definition()]
```

**After (tool_registry.py):**
```python
registry = get_tool_registry()
# Auto-registers default tools
tools = registry.get_all_tool_definitions()
```

### 5. Logging

**Before:**
```python
# Print statements
print(sparql_query)
```

**After:**
```python
from src.utils.logging_config import get_logger
logger = get_logger("module_name")
logger.info("Message", extra_data)
```

## Breaking Changes

### Import Paths

**Before:**
```python
from models import ChatHistory
from graph_rag_tool import GraphDBTool
```

**After:**
```python
from src.models.chat_models import ChatHistory
from src.tools.graphdb_tool import GraphDBTool
```

### Entry Point

**Before:**
```bash
python app.py
```

**After:**
```bash
python src/web/app.py
# or
python -m src.web.app
```

### Environment Variables

No changes to `.env` file format, but now accessed through `config` object.

## New Features

### 1. Middleware Support

```python
# Custom middleware
class CustomMiddleware:
    def before_request(self, session_id, message):
        # Pre-processing logic
        pass

agent.middleware.add_middleware(CustomMiddleware())
```

### 2. Tool Registry

```python
# Register custom tool
registry.register_tool(
    name="my_tool",
    tool_definition={...},
    tool_function=my_function
)
```

### 3. Context Provider

```python
context_provider = get_context_provider()
context = context_provider.get_or_create_context(session_id)
summary = context_provider.get_conversation_summary(session_id)
```

### 4. Checkpointing (Future)

```python
checkpoint = thread_manager.create_checkpoint(session_id)
# Save checkpoint to database
...
# Restore later
thread_manager.restore_checkpoint(checkpoint)
```

### 5. Enhanced Error Handling

```python
try:
    result = tool.execute(query)
except ConnectionError as e:
    # Specific error handling
    logger.error(f"Connection failed: {e}")
```

### 6. New API Endpoints

- `/agent/info` - Get agent information
- `/session/info` - Get session information
- `/health` - Health check

## Testing Changes

### Before

No formal test structure.

### After

```
tests/
├── unit/
│   ├── test_agents.py
│   ├── test_tools.py
│   └── test_services.py
└── integration/
    ├── test_agent_integration.py
    └── test_graphdb_integration.py
```

## Configuration Changes

### New Files

1. **config/agent_config.json**: Agent-specific configuration
2. **config/logging_config.json**: Logging settings (planned)

### Modified Files

1. **.env**: No changes, still used for secrets

## Dependencies

### New Requirements

```
# Will be added in Phase 10
agent-framework  # When fully integrated
```

### Existing Requirements

No changes to existing dependencies (Flask, Pydantic, Azure OpenAI, etc.)

## Migration Checklist

- [x] Phase 1: Directory structure
- [x] Phase 2: Configuration layer
- [x] Phase 3: Models refactoring
- [x] Phase 4: Services layer
- [x] Phase 5: Tools refactoring
- [x] Phase 6: Context management
- [x] Phase 7: Agent implementation
- [x] Phase 8: Web layer
- [x] Phase 9: Documentation
- [ ] Phase 10: Testing & validation

## Rollback Plan

If issues arise:

1. **Git Reset**:
   ```bash
   git reset --hard HEAD~1
   ```

2. **Keep New Structure, Restore Old Logic**:
   - Keep new directory structure
   - Restore old `app.py` and `llm_service.py`
   - Update imports

3. **Partial Rollback**:
   - Rollback specific components
   - Keep working parts

## Testing After Migration

### 1. Smoke Tests

```bash
# Check imports
python -c "from src.agents.jaguar_agent import get_jaguar_agent"

# Check Flask app
python -c "from src.web.app import create_app; app = create_app()"
```

### 2. Functional Tests

1. Start the application
2. Test chat interface
3. Test SPARQL queries
4. Test history
5. Test clear function

### 3. Integration Tests

1. GraphDB connection
2. Azure OpenAI connection
3. Tool execution
4. Session management

## Performance Impact

### Expected Changes

- **Startup time**: Slightly slower (more modules)
- **Response time**: Similar or slightly better (caching)
- **Memory usage**: Slightly higher (more objects)

### Monitoring

- Check logs for timing information
- Monitor session count
- Track tool execution times

## Known Issues

### 1. Agent Framework Package

- **Issue**: Agent Framework is in preview, package name uncertain
- **Workaround**: Using compatible patterns without full framework integration
- **Resolution**: Update when framework is stable

### 2. Import Paths

- **Issue**: All imports now use `src.` prefix
- **Resolution**: Update PYTHONPATH or use `python -m` execution

### 3. Template Path

- **Issue**: Templates moved to `src/web/templates/`
- **Resolution**: Flask configured with correct template folder

## Future Migration Steps

### Phase 11: Full Agent Framework Integration

When Agent Framework is production-ready:

1. Install `microsoft-agent-framework`
2. Inherit from `Agent` base class
3. Use Agent Framework's native threading
4. Implement Agent Framework workflows

### Phase 12: Multi-Agent System

1. Add specialized agents
2. Implement workflow orchestration
3. Add human-in-the-loop patterns

## Support & Resources

- **Documentation**: `/docs/` directory
- **Architecture**: `docs/architecture.md`
- **Agent Design**: `docs/agent_design.md`
- **Original README**: `README.md` (updated)

## Questions & Feedback

For questions about this migration:
1. Review architecture documentation
2. Check agent design docs
3. Examine code comments
4. Review git commit history

