# GraphRAG Chatbot — Knowledge Graph Question Answering

A Python-based GraphRAG (Graph Retrieval-Augmented Generation) chatbot that combines a knowledge graph with a large language model to answer questions using retrieved graph evidence.

The project provides a Streamlit web interface where users can ask questions in natural language and explore information stored in a Neo4j knowledge graph.

## Features

- **Interactive web UI:** Chat with the assistant through Streamlit.
- **Knowledge graph retrieval:** Retrieve relevant nodes and relationships from Neo4j AuraDB.
- **Graph analysis:** Use NetworkX to build and inspect retrieved subgraphs.
- **LLM-powered answers:** Use LangChain and OpenAI to generate responses grounded in retrieved evidence.
- **Conversation memory:** Use recent conversation messages to help interpret follow-up questions during a session.
- **Environment-based configuration:** Store API keys and database credentials in environment variables.

## Technology Stack

- Python
- Streamlit
- Neo4j AuraDB
- NetworkX
- LangChain
- LangChain OpenAI integration
- python-dotenv
- OpenAI API

## Project Structure

```text
Knowledge-Graph-GraphRAG/
├── app.py
├── langchain_graphrag_chatbot.py
├── schemes_graph.graphml
├── schemes_graph_visualization.png
├── schemes_graph_from_neo4j.graphml
├── schemes_graph_from_neo4j.png
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

Some generated graph files may be optional. Include only the files that are useful and safe to share.

## Prerequisites

- Python 3.10 or a compatible version for your installed dependencies
- A Neo4j AuraDB instance or another accessible Neo4j database
- An OpenAI API key with API access and available quota
- Git, if you want to upload the project to GitHub

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace the URL with your actual GitHub repository URL.

### 2. Create a virtual environment

Windows:

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```cmd
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file in the project root:

```env
NEO4J_URI=your_neo4j_uri
NEO4J_USERNAME=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password
NEO4J_DATABASE=neo4j
OPENAI_API_KEY=your_openai_api_key
```

Replace the example values with your own credentials. Never commit `.env` to GitHub.

### 5. Start the web application

```cmd
python -m streamlit run app.py
```

Open the local URL printed in your terminal, usually:

http://localhost:8501

## How It Works

1. The user submits a question through the Streamlit interface.
2. The application uses recent conversation history to help interpret the question.
3. The retrieval component searches Neo4j for matching graph nodes and their connections.
4. NetworkX constructs a subgraph from the retrieved nodes and relationships.
5. LangChain sends the question and retrieved evidence to the configured OpenAI model.
6. The model generates an answer based on the available evidence.
7. The application displays the answer and retains recent conversation messages for follow-up questions.

## Security Notes

- Do not upload `.env`, API keys, database passwords, or other secrets.
- Keep the Neo4j database credentials private.
- Review graph data and generated files before making the repository public.
- Configure appropriate Neo4j permissions and database access restrictions.
- OpenAI API usage may incur charges depending on your account and usage.

## Limitations

- Answer quality depends on the completeness and accuracy of the knowledge graph.
- Keyword-based retrieval may miss relevant information when different terminology is used.
- The chatbot cannot reliably answer questions about facts that are absent from the retrieved evidence.
- Conversation memory is session-based and is not permanent storage.

## Future Improvements

- Add semantic or vector-based graph retrieval.
- Add an interactive knowledge graph visualization.
- Improve entity matching and relationship-aware retrieval.
- Add persistent conversation history.
- Add automated tests and structured logging.
- Deploy the application to a hosted environment.

## License

Choose a license before distributing this project. If you intend to make the repository open source, consider adding an appropriate license file.
