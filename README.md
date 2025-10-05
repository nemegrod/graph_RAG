# 🐆 Graph RAG Chat Application

A production-ready **Graph RAG (Retrieval-Augmented Generation)** chat application that combines the power of **Azure OpenAI GPT** with **knowledge graphs** stored in **Ontotext GraphDB**. This application demonstrates how to build an intelligent assistant that can query structured data using SPARQL and provide natural language responses.

## 🌟 Features

### 🤖 **Intelligent LLM Integration**
- **Azure OpenAI GPT-5** powered conversational interface
- **Function calling** for dynamic SPARQL query generation
- **Context-aware** responses based on graph data
- **Markdown rendering** with syntax highlighting for code blocks

### 🔗 **Graph RAG Architecture**
- **GraphDB integration** with Ontotext GraphDB
- **LLM-driven SPARQL generation** based on ontology
- **Hybrid intelligence** combining structured knowledge graphs with LLM reasoning
- **Real-time data retrieval** from triple store

### 📊 **Jaguar Conservation Database**
- **jaguar ontology** with some classes and properties for demo purpouses
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

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
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
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_MODEL_DEPLOYMENT=your_model_deployment_name

# GraphDB Configuration
GRAPHDB_URL=http://localhost:7200
GRAPHDB_REPOSITORY=Jaguars
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
3. Import the ontology file: `jaguar_ontology_rich.ttl`
4. Import the assets file: `jaguars.ttl`

### 7. Run the Application

```bash
python3 app.py
```

Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
graph_RAG/
├── app.py                      # Flask application entry point
├── llm_service.py              # Azure OpenAI integration & orchestration
├── graph_rag_tool.py           # GraphDB SPARQL query tool
├── models.py                   # Pydantic models (ChatHistory, Message)
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in repo)
├── .gitignore                  # Git ignore rules
├── jaguar_ontology_rich.ttl    # Rich jaguar ontology schema
├── templates/
│   └── chat.html              # Main chat interface (Jinja2 template)
└── README.md                   # This file
```

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0** - Lightweight web framework
- **Pydantic 2.5.0** - Data validation using Python type annotations
- **Azure OpenAI 1.51.0** - GPT-5 API client
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

## 💡 How It Works

1. **User Interaction** - User asks a question about jaguars
2. **LLM Analysis** - Azure OpenAI GPT analyzes the question
3. **Function Calling** - GPT generates a SPARQL query based on the ontology
4. **SPARQL Execution** - Query executes against GraphDB
5. **Data Processing** - Raw JSON results returned to LLM
6. **Natural Language Response** - GPT interprets and formats the response
7. **Markdown Rendering** - Frontend renders with formatting and highlighting

## 📊 Example Queries

- "How many jaguars are in the database?"
- "Tell me about female jaguars that were orphaned"
- "Which conservation organizations are working in Brazil?"
- "What are the main threats to jaguar populations?"
- "Show me jaguars that were rescued and later released"

## 🔒 Security

- API keys stored in `.env` (excluded from version control)
- Environment variables for all sensitive configuration
- `.gitignore` configured to protect credentials
- No hardcoded secrets in source code

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Niklas** - [GitHub](https://github.com/nemegrod)

---

**Built with ❤️ using Graph RAG, Azure OpenAI, and GraphDB**
