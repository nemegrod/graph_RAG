# 🐆 Graph RAG Chat Application

A **Graph RAG (Retrieval-Augmented Generation)** chat application that combines **OpenAI GPT** with **knowledge graphs** stored in **GraphDB**. This application demonstrates how to build an intelligent assistant using **Microsoft Agent Framework** with structured data using SPARQL.

**Version 2.0** - Single-file POC demonstrating Graph RAG capabilities with Agent Framework integration.

## 🌟 Graph RAG Features

### 🤖 **Intelligent AI Agent**
- **Microsoft Agent Framework** for conversation management
- **OpenAI GPT-4** powered conversational interface
- **Function calling** for dynamic SPARQL query generation
- **Context-aware** responses based on graph data
- **Thread-based state management** for conversation persistence

### 🔗 **Graph RAG Architecture**
- **GraphDB integration** with RDF triple store
- **LLM-driven SPARQL generation** based on jaguar ontology
- **Hybrid intelligence** combining structured knowledge graphs with LLM reasoning
- **Real-time data retrieval** from knowledge graph
- **Natural language to SPARQL** query translation

### 📊 **Jaguar Conservation Database**
- **Jaguar ontology** with classes and properties
- Individual jaguar tracking (gender, identification marks, monitoring dates)
- Conservation efforts and organizations
- Threats, habitats, and locations
- Rescue, rehabilitation, and release data

### 🎨 **Simple Web Interface**
- **Flask-based** web application
- **Clean chat interface** with message history
- **Error handling** and user feedback
- **Form-based** interaction (no JavaScript complexity)

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (Python 3.10+ recommended)
- **GraphDB** running on localhost:7200
- **OpenAI API** access
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

### 4. Configure Environment Variables

Create a `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_RESPONSES_MODEL_ID=gpt-4

# GraphDB Configuration
GRAPHDB_URL=http://localhost:7200
GRAPHDB_REPOSITORY=your_repo_name_here
```

### 5. Start GraphDB

```bash
# Using Docker (first time)
docker run -d --name graphdb-instance -p 7200:7200 local-graphdb:latest

# Stop container
docker stop graphdb-instance

# Start existing container
docker start graphdb-instance

```

### 6. Load Jaguar Ontology

1. Access GraphDB Workbench at `http://localhost:7200`
2. Create a new repository named `jaguar_conservation`
3. Import the ontology file: `data/ontologies/jaguar_ontology.ttl`

### 7. Run the Application

```bash
# Start the single-file Flask application
python3 app.py
```

Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

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
