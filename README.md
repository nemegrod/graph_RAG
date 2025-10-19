# 🐆 Graph RAG Chat Application

A **Graph RAG (Retrieval-Augmented Generation)** chat application that combines the power of **Azure OpenAI GPT** with **knowledge graphs** stored in **Ontotext GraphDB**. This application demonstrates how to build an intelligent assistant using **Microsoft Agent Framework patterns** with structured data using SPARQL.

**Version 2.0** - Refactored with Agent Framework architecture for scalability and enterprise readiness.

## 🌟 Features

### 🤖 **Intelligent AI Agent**
- **Agent Framework patterns** for modular, scalable architecture
- **Azure OpenAI GPT** powered conversational interface
- **Function calling** for dynamic SPARQL query generation
- **Context-aware** responses based on graph data
- **Middleware support** for logging, telemetry, and filtering
- **Thread-based state management** for robust conversation handling

### 🔗 **Graph RAG Architecture**
- **GraphDB integration** with Ontotext GraphDB
- **LLM-driven SPARQL generation** based on ontology
- **Hybrid intelligence** combining structured knowledge graphs with LLM reasoning
- **Real-time data retrieval** from triple store
- **Tool registry** for extensible functionality

### 📊 **Jaguar Conservation Database**
- **Jaguar ontology** with classes and properties
- Individual jaguar tracking (gender, identification marks, monitoring dates)
- Conservation efforts and organizations
- Threats, habitats, and locations
- Rescue, rehabilitation, and release data

### 🎨 **Modern UI/UX**
- **Bootstrap 5** responsive design
- **Full-height chat interface** that adapts to browser window
- **Real-time markdown formatting** with Marked.js
- **Code syntax highlighting** with Prism.js
- **Typing indicators** and smooth animations

### 🏗️ **Enterprise Architecture**
- **Layered architecture** with clear separation of concerns
- **Modular components** (agents, tools, services, models)
- **Configuration management** with JSON and environment variables
- **Comprehensive logging** with file and console outputs
- **Testing structure** with unit and integration tests
- **Documentation** for architecture and design decisions

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** ⚠️ **REQUIRED** for Microsoft Agent Framework
- **Docker** (for GraphDB)
- **Azure OpenAI API** access
- **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/nemegrod/graph_RAG.git
cd graph_RAG
```

### 2. Set Up Virtual Environment

```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

For development:
```bash
pip install -r requirements-dev.txt
```

### 4. Configure Environment Variables

Run the setup script:
```bash
python scripts/setup_environment.py
```

Or manually create a `.env` file:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_MODEL_DEPLOYMENT=your_model_deployment_name

# GraphDB Configuration
GRAPHDB_URL=http://localhost:7200
GRAPHDB_REPOSITORY=Jaguars

# Flask Configuration (optional)
FLASK_SECRET_KEY=your-secret-key-change-this-in-production
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### 5. Start GraphDB

```bash
# Pull GraphDB image
docker pull ontotext/graphdb:10.7.3

# Run GraphDB
docker run --name graphdb-local -p 7200:7200 -d ontotext/graphdb:10.7.3

# Start existing container
docker start graphdb-local
```

### 6. Load Jaguar Ontology

1. Access GraphDB Workbench at `http://localhost:7200`
2. Create a new repository named `Jaguars`
3. Import the ontology file: `data/ontologies/jaguar_ontology_rich.ttl`
4. Import the data file: `data/ontologies/jaguars.ttl`

### 7. Run the Application

```bash
# Using the helper script
python scripts/start_app.py

# Or directly
python src/web/app.py
```

Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
graph_RAG/
├── src/
│   ├── agents/              # AI agents
│   │   └── jaguar_agent/    # Jaguar conservation agent
│   ├── tools/               # Agent tools (GraphDB, etc.)
│   ├── services/            # External services (LLM, GraphDB)
│   ├── models/              # Data models
│   ├── context/             # State and context management
│   ├── web/                 # Flask application
│   │   ├── app.py          # Application factory
│   │   ├── routes.py       # API routes
│   │   └── templates/      # HTML templates
│   ├── workflows/           # Future: Multi-agent workflows
│   └── utils/               # Utilities and configuration
├── data/
│   ├── ontologies/          # RDF/Turtle ontology files
│   └── corpus/              # Text corpus files
├── config/
│   └── agent_config.json    # Agent configuration
├── tests/
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── docs/                    # Documentation
│   ├── architecture.md
│   ├── agent_design.md
│   └── migration_notes.md
├── scripts/                 # Helper scripts
├── logs/                    # Log files
├── .env                     # Environment variables (not in repo)
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── pyproject.toml           # Modern Python packaging
└── README.md               # This file
```

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0** - Lightweight web framework
- **Pydantic 2.5.0** - Data validation using Python type annotations
- **Azure OpenAI 1.51.0** - GPT API client
- **Requests** - HTTP library for GraphDB communication
- **python-dotenv** - Environment variable management

### Frontend
- **Bootstrap 5** - Responsive UI framework
- **Marked.js** - Markdown parsing and rendering
- **Prism.js** - Syntax highlighting for code blocks
- **Vanilla JavaScript** - No heavy frameworks, pure performance

### Data Layer
- **Ontotext GraphDB 10.7.3** - RDF triple store
- **SPARQL** - Query language for RDF data
- **RDF/Turtle** - Ontology definition format

### Architecture
- **Microsoft Agent Framework patterns** - Modular agent architecture
- **Layered architecture** - Clear separation of concerns
- **Middleware pattern** - Cross-cutting concerns
- **Registry pattern** - Tool discovery and management

## 💡 How It Works

1. **User Interaction** - User asks a question about jaguars
2. **Agent Processing** - Jaguar Agent analyzes the question
3. **Middleware** - Logging and telemetry middleware invoked
4. **Tool Selection** - Agent decides to use GraphDB tool
5. **SPARQL Generation** - GPT generates a SPARQL query based on the ontology
6. **Query Execution** - Query executes against GraphDB
7. **Data Processing** - Raw JSON results returned to agent
8. **Natural Language Response** - Agent interprets and formats the response
9. **State Management** - Conversation history saved in thread
10. **Markdown Rendering** - Frontend renders with formatting and highlighting

## 📊 Example Queries

- "How many jaguars are in the database?"
- "Tell me about female jaguars that were orphaned"
- "Which conservation organizations are working in Brazil?"
- "What are the main threats to jaguar populations?"
- "Show me jaguars that were rescued and later released"

## 🧪 Testing

### Run All Tests

```bash
# Using the script (Unix/Linux/Mac)
./scripts/run_tests.sh

# Windows
python -m pytest tests/

# With coverage
pytest --cov=src --cov-report=html
```

### Run Specific Tests

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/test_graphdb_tool.py
```

## 📚 Documentation

- **[Architecture](docs/architecture.md)** - System architecture and design
- **[Agent Design](docs/agent_design.md)** - Jaguar Agent design and usage
- **[Migration Notes](docs/migration_notes.md)** - Migration from v1.0 to v2.0

## 🔒 Security

- API keys stored in `.env` (excluded from version control)
- Environment variables for all sensitive configuration
- `.gitignore` configured to protect credentials
- No hardcoded secrets in source code
- Session-based access control
- Input validation and sanitization

## 🚀 Deployment

### Development
```bash
python scripts/start_app.py
```

### Production
Consider using:
- **Gunicorn** or **uWSGI** as WSGI server
- **Nginx** as reverse proxy
- **Redis** for session storage
- **Docker Compose** for containerization

Example with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 src.web.app:app
```

## 🔮 Future Enhancements

### Planned Features
- [ ] **Full Microsoft Agent Framework integration** (when production-ready)
- [ ] **Multi-agent workflows** for complex queries
- [ ] **Streaming responses** for real-time feedback
- [ ] **Checkpointing** for long-running conversations
- [ ] **Human-in-the-loop** patterns
- [ ] **Additional tools** (web search, document analysis, visualization)
- [ ] **Authentication** and user management
- [ ] **API documentation** with OpenAPI/Swagger

### Scalability
- [ ] **Distributed sessions** with Redis
- [ ] **Horizontal scaling** with load balancing
- [ ] **Async processing** with Celery
- [ ] **Caching layer** for frequent queries
- [ ] **Message queue** for async operations

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Niklas** - [GitHub](https://github.com/nemegrod)

## 🙏 Acknowledgments

- **Microsoft Agent Framework** - Architecture patterns and inspiration
- **Ontotext GraphDB** - Powerful RDF triple store
- **Azure OpenAI** - Advanced language models
- **Flask** - Lightweight web framework

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the documentation in `/docs`
- Review the migration notes for v2.0 changes

---

**Built with ❤️ using Graph RAG, Azure OpenAI, GraphDB, and Microsoft Agent Framework patterns**

**Version 2.0** - Agent Framework Architecture  
**Previous Version**: v1.0 - Simple flat structure
