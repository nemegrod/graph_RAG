# Jaguar Conservation Agent Design

## Overview

The Jaguar Conservation Agent is a **Semantic Graph RAG (Retrieval-Augmented Generation)** system that combines **OpenAI GPT** with **RDF knowledge graphs** to provide intelligent conservation insights. This system demonstrates:

1. **Conversational AI** using **Microsoft Agent Framework DevUI** that queries knowledge graphs with SPARQL
2. **Ontology-Aware Knowledge Extraction** that transforms unstructured text into structured RDF data

This is **true semantic Graph RAG** using formal ontologies (RDFS/OWL), not labeled property graphs (LPG). The system showcases why ontologies are essential for intelligent knowledge representation and extraction.

## Dual Capabilities: Query & Extract

### 1. Graph RAG Query Capabilities
- **Knowledge Graph Integration**: Direct SPARQL queries against GraphDB triple store
- **LLM-Driven Query Generation**: AI automatically generates SPARQL from natural language
- **Hybrid Intelligence**: Combines structured graph data with LLM reasoning
- **Real-time Data Retrieval**: Live queries against jaguar conservation database
- **Context-Aware Responses**: Maintains conversation context across queries

### 2. Ontology-Aware Knowledge Extraction
- **Semantic Entity Disambiguation**: Distinguishes wildlife jaguars from cars and guitars
- **Concept Understanding**: Uses formal ontologies to understand domain context
- **Automated RDF Generation**: Creates valid Turtle syntax aligned with ontology
- **Relationship Inference**: Discovers implicit connections between entities
- **Zero Post-Processing**: Extracts clean, structured data without manual cleanup

### Agent Characteristics
- **Name**: JaguarQueryAgent
- **Role**: Graph RAG specialist for jaguar conservation
- **Domain**: Jaguar population, conservation, habitats, threats
- **Architecture**: Microsoft Agent Framework with DevUI integration

### Capabilities
1. **SPARQL Query Generation**: Convert natural language to SPARQL queries
2. **Graph Data Interpretation**: Understand complex ontology structures
3. **Natural Language Responses**: Generate human-readable answers from graph data
4. **Conversation Context**: Maintain chat history and context
5. **Markdown Formatting**: Rich text responses with code blocks and formatting

## Architecture

### Simplified PoC Architecture with DevUI

```
┌─────────────────────────────────────────┐
│        Microsoft Agent Framework         │
│  ┌─────────────────────────────────┐    │
│  │           DevUI Server           │    │
│  │  - Auto-opening Browser          │    │
│  │  - Interactive Chat Interface    │    │
│  │  - Built-in Debugging           │    │
│  │  - Real-time Responses          │    │
│  └─────────────────────────────────┘    │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│        Agent Framework                  │
│  ┌─────────────────────────────────┐    │
│  │    Jaguar Query Agent           │    │
│  │  ┌─────────────────────────┐    │    │
│  │  │    System Prompt        │    │    │
│  │  │  - Graph RAG Context    │    │    │
│  │  │  - SPARQL Guidelines    │    │    │
│  │  │  - Response Formatting  │    │    │
│  │  └─────────────────────────┘    │    │
│  │                                 │    │
│  │  ┌─────────────────────────┐    │    │
│  │  │    OpenAI Client        │    │    │
│  │  │  - GPT-4 Integration    │    │    │
│  │  │  - Function Calling     │    │    │
│  │  │  - Thread Management    │    │    │
│  │  └─────────────────────────┘    │    │
│  │                                 │    │
│  │  ┌─────────────────────────┐    │    │
│  │  │    GraphDB Tool         │    │    │
│  │  │  - SPARQL Execution     │    │    │
│  │  │  - Query Validation     │    │    │
│  │  │  - Result Processing    │    │    │
│  │  └─────────────────────────┘    │    │
│  └─────────────────────────────────┘    │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│           External Systems              │
│  ┌─────────────────┐  ┌─────────────┐  │
│  │   OpenAI API    │  │  GraphDB     │  │
│  │   - GPT-4       │  │  - RDF Store │  │
│  │   - Responses   │  │  - SPARQL    │  │
│  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────┘
```

## Graph RAG System Prompt

The agent uses a carefully crafted system prompt optimized for Graph RAG:

### Core Instructions
1. **Graph RAG Focus**: Always use the GraphDB tool for jaguar-related queries
2. **SPARQL Generation**: Convert natural language to valid SPARQL queries
3. **Ontology Awareness**: Base queries on the provided jaguar ontology
4. **Response Formatting**: Use markdown with code blocks for SPARQL
5. **Data Attribution**: Always mention that information comes from the jaguar database

### Key Guidelines
- Form simple queries first, add complexity only if needed
- Show the SPARQL query once in each response
- Use **bold** for emphasis when appropriate
- Use bullet points or numbered lists for multiple items
- Break up long responses into paragraphs
- Be concise but comprehensive in answers

## Graph RAG Tool Integration

### GraphDB Tool - Core Graph RAG Component

The agent's primary tool for knowledge graph retrieval:

**Function Name**: `query_jaguar_database`

**Purpose**: Execute SPARQL queries against the jaguar conservation knowledge graph

**Parameters**:
- `sparql_query`: SPARQL query string generated by the LLM

**Ontology Coverage**:
- **Classes**: Jaguar, Habitat, Location, Threat, ConservationEffort, Organization
- **Properties**: hasGender, wasKilled, rescuedBy, facesThreat, hasLocation, etc.
- **Relationships**: Complex conservation data relationships

### Graph RAG Query Examples

```sparql
# Count total jaguars in database
SELECT (COUNT(?jaguar) as ?count) WHERE { 
  ?jaguar a :Jaguar . 
}

# Find jaguars by gender with labels
SELECT ?jaguar ?label ?gender WHERE { 
  ?jaguar a :Jaguar . 
  OPTIONAL { ?jaguar rdfs:label ?label . } 
  OPTIONAL { ?jaguar :hasGender ?gender . } 
}

# Find jaguars that were killed with cause of death
SELECT ?jaguar ?label ?causeOfDeath WHERE { 
  ?jaguar a :Jaguar . 
  ?jaguar :wasKilled true . 
  OPTIONAL { ?jaguar rdfs:label ?label . } 
  OPTIONAL { ?jaguar :causeOfDeath ?causeOfDeath . } 
}

# Find conservation efforts by organization
SELECT ?effort ?org ?description WHERE {
  ?effort a :ConservationEffort .
  ?effort :conductedBy ?org .
  ?effort rdfs:label ?description .
  ?org a :Organization .
}
```

## Graph RAG Processing Flow

### 1. DevUI Launch
```python
# main.py starts DevUI server
from agent_framework.devui import serve
from src.agents.jaguar_query_agent import create_jaguar_query_agent

query_agent = create_jaguar_query_agent()
serve(entities=[query_agent], auto_open=True)
```

### 2. User Interaction via DevUI
- **Auto-opening Browser**: DevUI launches at `http://localhost:8000`
- **Interactive Chat**: User types queries in the DevUI interface
- **Real-time Responses**: Immediate feedback and conversation flow

### 3. Graph RAG Query Generation
- **LLM Analysis**: OpenAI GPT analyzes the user's natural language query
- **SPARQL Generation**: AI generates appropriate SPARQL query for GraphDB
- **Ontology Mapping**: Maps user intent to jaguar ontology classes/properties

### 4. Knowledge Graph Query Execution
- **Tool Call Detection**: Agent Framework detects need for GraphDB tool
- **SPARQL Execution**: `query_jaguar_database` tool executes query against GraphDB
- **Result Processing**: Raw SPARQL results are processed and formatted

### 5. Response Generation
- **LLM Interpretation**: OpenAI GPT interprets GraphDB results
- **Natural Language Response**: Generates human-readable response
- **Markdown Formatting**: Applies formatting with code blocks for SPARQL

### 6. Context Preservation
- **Thread Management**: Agent Framework maintains conversation context
- **DevUI History**: Built-in conversation history in DevUI interface
- **State Persistence**: Conversation state preserved across requests

## Graph RAG State Management

### DevUI State Management
```python
# DevUI handles all state management automatically
# No manual state configuration required
serve(entities=[query_agent], auto_open=True)
```

### Thread Management
- **Agent Framework**: Microsoft Agent Framework manages conversation context
- **OpenAI Responses API**: Server-side thread persistence
- **DevUI Interface**: Built-in conversation history and state management

### Chat History
- **Agent Framework**: Maintains conversation context for LLM
- **DevUI**: Built-in conversation history display
- **Persistence**: Thread state preserved across requests automatically

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
# Hardcoded in create_jaguar_query_agent()
settings = OpenAISettings(
    api_key=os.getenv("OPENAI_API_KEY", ""),
    model_id=os.getenv("OPENAI_RESPONSES_MODEL_ID", "gpt-4")
)
```

## Graph RAG Response Formatting

The agent applies Graph RAG-specific formatting:
1. **SPARQL Display**: Show generated query in code blocks
2. **Data Attribution**: Always mention jaguar database source
3. **Markdown Formatting**: Use **bold**, bullet points, code blocks
4. **Structured Responses**: Break complex answers into paragraphs

## Error Handling

### Graph RAG Error Levels

1. **SPARQL Errors**: Invalid query syntax, ontology mismatches
2. **GraphDB Errors**: Connection failures, query timeouts
3. **LLM Errors**: OpenAI API failures, rate limits
4. **Web Errors**: Flask request/response errors

### Error Response Format
```python
# DevUI handles error display automatically
# Errors are shown in the DevUI interface
# No manual error handling required
```

## Graph RAG Usage Examples

### Running the Application
```bash
# Start the DevUI application
python3 main.py

# DevUI automatically opens at http://localhost:8000
```

### Example Queries
Try these Graph RAG queries in the DevUI interface:

**Basic Queries:**
- "How many jaguars are in the database?"
- "Show me all female jaguars"
- "What conservation efforts are being conducted?"

**Complex Queries:**
- "Find jaguars that were killed and their causes of death"
- "Which organizations are conducting conservation efforts?"
- "Show me jaguars by location and their monitoring dates"

### Programmatic Usage
```python
# Direct agent usage (if needed)
from src.agents.jaguar_query_agent import create_jaguar_query_agent
import asyncio

agent = create_jaguar_query_agent()
thread = agent.get_new_thread()

# Run a query
response = asyncio.run(agent.run(
    "How many jaguars are in the database?", 
    thread=thread, 
    store=True
))
print(response.text)
```

## Ontology-Aware Knowledge Extraction

### The "Jaguar Problem" - Extreme Edition

The system includes a Jupyter notebook (`text2knowledge.ipynb`) that demonstrates **ontology-driven extraction** against an extreme challenge:

**Corpus**: The complete "Oliver Twist" novel (~956,000 characters) containing:
- 📚 Victorian fiction as massive noise (200,000+ tokens)
- 🐆 Wildlife jaguar conservation data scattered throughout
- 🚗 Jaguar car mentions as deliberate distractors
- 🎸 Fender Jaguar guitar references to test disambiguation

**Solution**: By providing **GPT-5.2** with the **RDF ontology directly** (not a text description), the LLM:
1. **Maintains attention** across the entire extended context window
2. **Understands the domain** from formal RDF class definitions
3. **Disambiguates entities** based on ontology structure
4. **Extracts only wildlife-related information** from scattered locations
5. **Generates RDF Turtle** perfectly aligned with the ontology
6. **Infers relationships** between entities from contextual clues

### Knowledge Extraction Process

```
1. Load RDF Ontology (jaguar_ontology.ttl)
   - Fed directly to GPT-5.2, no text conversion
   - LLMs understand RDF natively from training
   ↓
2. Load Extreme Corpus (oliver_twist_corpus.txt)
   - 956K characters of novel + scattered jaguar data
   - Includes car and guitar distractors
   ↓
3. GPT-5.2 Semantic Analysis
   - Maintains attention across 200K+ tokens
   - Understands domain from RDF classes/properties
   - Disambiguates wildlife from cars/guitars
   - Identifies scattered relevant entities
   ↓
4. Generate RDF Turtle
   - Valid syntax
   - Aligned with ontology
   - Proper URIs and datatypes
   ↓
5. Import to GraphDB
   - Use "Import → Text snippet"
   - Data integrates seamlessly with existing graph
```

### Why RDF Ontologies (Not Text Descriptions)

**This requires RDF ontologies fed directly to the LLM**—not natural language descriptions:

✅ **Direct RDF Comprehension**
- LLMs are trained on vast RDF/OWL corpora
- They parse Turtle syntax like programming code
- No lossy translation from ontology → text → LLM

✅ **No Error Multiplication**
- Converting RDF to text introduces ambiguity
- Each translation step is a potential error source
- Direct RDF eliminates the "telephone game"

✅ **Machine-Readable Storage**
- RDF ontologies live in triple stores
- SPARQL queries work against the same structure
- One source of truth for humans, LLMs, and machines

✅ **LLMs "Simulate" OWL Reasoning**
- Whether LLMs truly reason is debatable
- But trained on so much RDF, they predict OWL-like outcomes
- Results demonstrate effective semantic understanding

**This CANNOT be done with LPG databases** because:
- LPG labels are just strings—no formal semantics
- No class hierarchies (RDFS/OWL inheritance)
- No property constraints (domain/range)
- LLMs have no semantic structure to reason over

### Extraction Example

**Input**: 956,000 characters including:
```
[200,000+ tokens of Oliver Twist novel...]

...El Jefe is an adult, male jaguar that was seen in Arizona...

[More novel chapters...]

...The Jaguar E-Type is a British sports car manufactured by Jaguar Cars...

[More novel chapters...]

...Conservation efforts in Sonora have tracked several wild jaguars...

[More novel chapters with Fender Jaguar guitar mentions...]
```

**Output RDF** (wildlife only, cars and guitars ignored):
```turtle
:ElJefe a ont:Jaguar ;
  rdfs:label "El Jefe" ;
  ont:hasGender "Male" ;
  ont:occursIn :Arizona ;
  ont:monitoredByOrg :AZGFD .
```

No cars. No guitars. No Victorian fiction. Just semantically relevant conservation data extracted from scattered locations across a massive corpus.

## Graph RAG Future Enhancements

### Advanced Graph RAG Features
1. **Multi-Modal Queries**: Combine text and image analysis
2. **Temporal Queries**: Time-based conservation trend analysis
3. **Geospatial Queries**: Location-based jaguar population mapping
4. **Predictive Analytics**: Conservation outcome predictions

### Knowledge Extraction Enhancements
1. **Multi-Domain Ontologies**: Extract from diverse sources
2. **Streaming Extraction**: Real-time knowledge mining
3. **Active Learning**: Improve extraction with user feedback
4. **Cross-Lingual Extraction**: Process multilingual corpora

### Knowledge Graph Enhancements
1. **Dynamic Ontology Updates**: Real-time ontology evolution
2. **Federated Queries**: Query multiple knowledge graphs
3. **Semantic Reasoning**: Advanced SPARQL reasoning capabilities
4. **Graph Visualization**: Interactive knowledge graph exploration

### Agent Framework Enhancements
1. **Multi-Agent Workflows**: Specialized agents for different tasks
2. **Streaming Responses**: Real-time Graph RAG query processing
3. **Human-in-the-Loop**: Query refinement and validation
4. **Memory Management**: Long-term conversation summarization

## Graph RAG Testing

### Manual Testing
1. **DevUI Interface**: Test queries through the DevUI
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

# Test complex queries
"Find conservation efforts in Arizona with their success rates"
```

## Graph RAG Performance

### Response Times
- **Simple Queries**: 2-3 seconds (count, basic filters)
- **Complex Queries**: 3-5 seconds (joins, aggregations)
- **No Tool Calls**: 1-2 seconds (general conversation)

### Optimization Strategies
1. **Query Caching**: Cache frequent SPARQL patterns
2. **Index Optimization**: Optimize GraphDB indexes
3. **Response Streaming**: Stream partial results
4. **Async Processing**: Non-blocking GraphDB queries

## Graph RAG Security

### SPARQL Injection Prevention
- **Query Validation**: Validate SPARQL syntax before execution
- **Parameter Escaping**: Properly escape user inputs
- **GraphDB Security**: Leverage GraphDB's built-in security

### Data Privacy
- **Read-Only Access**: Agent only reads from GraphDB
- **No Data Storage**: No user data persisted beyond conversation
- **Secure APIs**: Use HTTPS for all external communications

