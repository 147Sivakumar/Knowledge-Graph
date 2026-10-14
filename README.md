# Tamil Nadu Government Schemes — Knowledge Graph + RAG Chatbot

A Python-based Knowledge Graph and Retrieval-Augmented Generation (RAG) chatbot that helps users explore information about government schemes published on the Tamil Nadu Government website.

The project combines structured scheme data, a NetworkX knowledge graph, keyword-based retrieval, and OpenAI-powered question answering to provide answers grounded in retrieved scheme records.

## Project Overview

Finding relevant information about government schemes can require navigating multiple records and understanding details such as beneficiaries, benefits, eligibility, departments, and application procedures.

This project builds a local knowledge graph from collected scheme records and integrates it with a RAG chatbot to make the information easier to explore using natural-language questions.

### Key Features

- **Government scheme data collection:** Collect scheme information from the Tamil Nadu Government website.
- **Structured JSON dataset:** Store scheme names, departments, beneficiaries, benefits, eligibility, application procedures, descriptions, and source URLs.
- **Knowledge graph construction:** Represent schemes and their relationships using NetworkX.
- **Graph retrieval:** Find schemes by keyword and retrieve connected entities and relationships.
- **RAG-based question answering:** Retrieve relevant records and pass them to an OpenAI model to generate contextual answers.
- **Source references:** Include official source URLs for schemes discussed in answers.
- **Data quality awareness:** Flag potentially inconsistent records for manual verification.
- **Graph visualization:** Generate a PNG visualization of the knowledge graph using Matplotlib.

## Architecture

```text
Tamil Nadu Government Website
             |
             v
     Scheme Data Collection
             |
             v
        schemes.json
             |
             v
    Knowledge Graph Builder
             |
             v
     schemes_graph.graphml
             |
             v
       Graph Retriever
             |
             v
User Question ---> RAG Chatbot
                       |
                       v
             Retrieve Relevant Records
                       |
                       v
               OpenAI Responses API
                       |
                       v
                Answer + Sources
```

The graph retriever supplies related graph facts to the chatbot alongside retrieved scheme records.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| NetworkX | Knowledge graph construction and querying |
| GraphML | Storage format for the graph |
| JSON | Structured scheme data |
| OpenAI API | Natural-language answer generation |
| Matplotlib | Knowledge graph visualization |
| Virtual environment (`venv`) | Python dependency isolation |

## Knowledge Graph Details

The current graph contains:

- **73 nodes**
- **175 edges**
- **54 scheme records**

The graph represents scheme records and their relationships with departments, beneficiaries, benefits, and data-quality review information.

Examples of relationships include:

- `REPORTED_AS_BELONGING_TO`
- `LISTS_BENEFICIARY`
- `REPORTS_BENEFIT`

The graph is stored in `schemes_graph.graphml`.

These counts describe the current project data and may change when the dataset or graph-building logic is updated.

## Project Structure

```text
Knowledge Graph/
│
├── inspect_website.py
├── inspect_detail.py
├── scrape_schemes.py
├── schemes.json
├── build_knowledge_graph.py
├── query_knowledge_graph.py
├── graph_retriever.py
├── rag_chatbot.py
├── schemes_graph.graphml
├── visualize_knowledge_graph.py
├── schemes_graph_visualization.png
└── README.md
```

## Prerequisites

- Python 3.12 or a compatible Python version
- An OpenAI API key
- Internet access for API requests and website access
- Windows CMD or another terminal

## Installation and Setup

### 1. Clone the repository

After uploading the project to GitHub, clone it using:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace the placeholder URL with your actual GitHub repository URL.

### 2. Create a virtual environment

On Windows CMD:

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```cmd
python -m pip install networkx matplotlib openai
```

If the project uses additional Python packages, install those as well. A `requirements.txt` file can be added to record the complete dependency list.

### 4. Configure the OpenAI API key

In Windows CMD, set your API key for the current terminal session:

```cmd
set OPENAI_API_KEY=your_api_key_here
```

Replace the placeholder locally with your actual key.

**Security:** Never commit your API key to GitHub or hard-code it in Python files. Use environment variables or another secure configuration method.

## How to Run the Project

Run these commands from the project directory, with the virtual environment activated.

### 1. Build the knowledge graph

If you need to regenerate the graph from the JSON dataset:

```cmd
python build_knowledge_graph.py
```

### 2. Query the knowledge graph

```cmd
python query_knowledge_graph.py
```

Follow the prompts provided by the script.

### 3. Retrieve related graph facts

```cmd
python graph_retriever.py
```

Enter a scheme name or keyword to retrieve matching schemes and their connected entities.

### 4. Visualize the graph

```cmd
python visualize_knowledge_graph.py
```

The visualization script loads `schemes_graph.graphml` and saves:

```text
schemes_graph_visualization.png
```

### 5. Start the RAG chatbot

Make sure the `OPENAI_API_KEY` environment variable is configured in the current CMD session.

Then run:

```cmd
python rag_chatbot.py
```

Ask questions about scheme details, beneficiaries, benefits, eligibility, or application procedures. The chatbot retrieves relevant records and uses the OpenAI API to generate answers.

Use `Ctrl + C` to stop a running chatbot when it is waiting for another question.

## Example Questions

Try asking:

- What benefits are available for farmers?
- Tell me about Training to Farmers.
- Who are the beneficiaries of Training of Farmers on Pulses Production Technologies?
- What is the eligibility for a particular scheme?
- How can I apply for a scheme?
- Tell me about Infrastructure subsidy for Privately Developed Industrial Estates.

Answers depend on the scheme records retrieved for each question. If the dataset does not contain enough information, the chatbot should communicate that limitation rather than inventing missing details.

## Data Quality and Limitations

This project is an experimental information-retrieval and question-answering system, not an official government service.

- Scheme information is based on collected records from the Tamil Nadu Government website.
- Retrieved content may be incomplete, outdated, or inconsistent.
- Some records have been flagged for manual review based on keyword checks. A flag indicates a need for verification, not proof that a record is incorrect.
- The source dataset currently reports the same department for all 54 records. This should be checked against the official scheme pages before relying on departmental classifications.
- Generated answers may contain errors. Verify eligibility, funding, deadlines, and application instructions against the relevant official source.
- An included source URL does not by itself establish that every detail in a generated answer has been independently verified.

## Future Improvements

Potential next steps include:

- Improve retrieval with semantic embeddings.
- Add vector search and hybrid graph-plus-text retrieval.
- Improve entity matching and relationship extraction.
- Add interactive knowledge graph visualization.
- Build a web interface for asking questions.
- Add automated data validation and source freshness checks.
- Create automated tests for graph construction and retrieval.
- Add a `requirements.txt` file and reproducible setup instructions.
- Improve answer citations so individual claims can be traced to source records.

## Data Source

Tamil Nadu Government — Scheme List:

https://www.tn.gov.in/scheme_list.php?dep_id=Mg==

Always consult the relevant official scheme page for the latest authoritative information.

## License

Choose an appropriate open-source license before publishing the repository. For example, the MIT License may be suitable if you want to permit reuse with attribution and its license conditions.

## Author

**Your Name**

Python | Knowledge Graphs | Retrieval-Augmented Generation (RAG) | Natural Language Processing

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
