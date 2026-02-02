# 🚀 Production Ready RAG System

A production-grade Retrieval Augmented Generation (RAG) system built with FastAPI, Inngest, Qdrant, and Google Gemini. This system allows you to ingest PDF documents, store their embeddings in a vector database, and query them using natural language with AI-powered responses.

<img width="851" height="769" alt="image" src="https://github.com/user-attachments/assets/d8f1af12-d861-4f3b-845d-6f0d3a59a84f" />


## ✨ Features

- **📄 PDF Ingestion**: Load and process PDF documents into searchable chunks
- **🔍 Vector Search**: Powered by Qdrant for fast similarity search
- **🤖 AI-Powered Q&A**: Uses Google Gemini for intelligent question answering
- **⚡ Async Workflows**: Built with Inngest for reliable, observable workflows
- **📊 Comprehensive Logging**: Full observability with emoji-rich logging
- **🎯 Production Ready**: Type-safe with Pydantic models and error handling

## 🏗️ Architecture

This system uses **[Inngest](https://www.inngest.com/)** - a workflow orchestration platform that provides:
- ⚡ **Event-driven workflows**: Trigger functions via events
- 🔄 **Automatic retries**: Built-in error handling and recovery
- 📊 **Observability**: Full visibility into workflow execution
- ⏱️ **Step management**: Break workflows into resumable steps
- 🎯 **Type safety**: Pydantic-based serialization

<img width="908" height="484" alt="image" src="https://github.com/user-attachments/assets/efdb6534-f849-4219-b130-4bbd6de6e3a7" />



```
┌─────────────┐
│  Streamlit  │ ← Web UI (Optional)
│     UI      │
└──────┬──────┘
       │
┌──────▼──────┐
│   FastAPI   │ ← REST API Entry Point
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Inngest   │ ← Workflow Engine (Orchestrates everything)
└──────┬──────┘
       │
       ├──► 📖 Ingest PDF Workflow
       │    ├─ Load & Chunk PDF
       │    ├─ Generate Embeddings (Gemini)
       │    └─ Store in Qdrant
       │
       └──► 🔍 Query PDF Workflow
            ├─ Embed Question (Gemini)
            ├─ Search Vector DB (Qdrant)
            └─ Generate Answer (Gemini)
```



### Why Inngest?

Unlike traditional REST APIs where you must manage retries, timeouts, and monitoring yourself, Inngest handles:
- **Durable execution**: If a step fails, it retries automatically
- **Step isolation**: Each step runs independently and can be retried
- **Built-in observability**: View every workflow execution in the Inngest dashboard
- **Easy debugging**: See exactly which step failed and why

<img width="1920" height="969" alt="Screenshot from 2026-01-30 23-23-47" src="https://github.com/user-attachments/assets/f4cb22b5-04ac-46db-bc68-8e2c8cf3f25a" />



## 📋 Prerequisites

- Python 3.13+
- Qdrant (running locally or remote)
- Google Gemini API Key
- Inngest Dev Server (for local development)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/faris771/Production-Ready-RAG
cd Prodution_Ready_RAG
```

### 2. Install Dependencies

Using `uv` (recommended):
```bash
uv sync
```

Or using `pip`:
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```env
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: If using Groq
GROQ_API_KEY=your_groq_api_key_here

# Qdrant Configuration (optional, defaults shown)
QDRANT_URL=http://localhost:6333
```

> **Note**: The `.env` file is already in `.gitignore` to keep your secrets safe.

### 4. Start Qdrant

#### Using Docker (recommended):
```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

#### Or install locally:
```bash
# See: https://qdrant.tech/documentation/quick-start/
```

### 5. Start Inngest Dev Server

In a separate terminal:
```bash
npx inngest-cli@latest dev
```

This will start the Inngest Dev Server at `http://localhost:8288`.

## 🚀 Usage

### 🐳 Using the Pre-built Docker Image (GitHub Packages)

**The easiest way to get started is to pull the pre-built Docker image from GitHub Container Registry!**

#### Pull and Run the Image

```bash
# Pull the latest image from GitHub Packages
docker pull ghcr.io/faris771/production-ready-rag:latest

# Run with environment variables
docker run -d \
  --name rag-app \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your_api_key_here \
  -e QDRANT_URL=http://qdrant:6333 \
  ghcr.io/faris771/production-ready-rag:latest
```

#### Use in Docker Compose

Update your `docker-compose.yml` to use the pre-built image:

```yaml
services:
  app:
    image: ghcr.io/faris771/production-ready-rag:latest
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - QDRANT_URL=http://qdrant:6333
    depends_on:
      qdrant:
        condition: service_healthy
```

**Available Image Tags:**
- `ghcr.io/faris771/production-ready-rag:latest` - Latest stable release from main branch
- `ghcr.io/faris771/production-ready-rag:main-<sha>` - Specific commit from main branch
- `ghcr.io/faris771/production-ready-rag:main` - Main branch (same as latest)

**Note:** The package is publicly available, so no authentication is required to pull the image. The authentication section below is only relevant if you fork this repository and make it private.

**Authentication (for private repositories):**
```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull the image
docker pull ghcr.io/faris771/production-ready-rag:latest
```

---

### 🐳 Running with Docker (Recommended for Production)

**Docker Compose makes it easy to run all services together!**

#### Option A: Without Streamlit UI

```bash
# 1. Make sure you have .env file with your API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 2. Start all services
docker-compose up -d

# 3. Start Inngest Dev Server (in separate terminal)
npx inngest-cli@latest dev
```

#### Option B: With Streamlit UI

```bash
# Start all services including Streamlit
docker-compose --profile with-ui up -d

# Start Inngest Dev Server (in separate terminal)
npx inngest-cli@latest dev
```

**Services will be available at:**
- 🚀 FastAPI: http://localhost:8000
- 🎨 Streamlit UI: http://localhost:8501 (if using --profile with-ui)
- 🔍 Qdrant: http://localhost:6333
- ⚡ Inngest: http://localhost:8288

**Useful Docker Commands:**
```bash
# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f app
docker-compose logs -f qdrant

# Stop all services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v

# Rebuild containers after code changes
docker-compose build
docker-compose up -d

# Check service status
docker-compose ps
```

**Why Docker?**
- ✅ Consistent environment across different machines
- ✅ Easy to deploy to production
- ✅ Automatic service dependencies (Qdrant starts before FastAPI)
- ✅ Health checks ensure services are ready
- ✅ One command to start/stop everything
- ✅ Isolated network for all services

---

### 🔧 Running Manually (Development)

For local development without Docker:

```bash
uvicorn main:app --reload --log-level info
```

The API will be available at `http://localhost:8000`.

### Quick Start with Streamlit UI 🎨

**For the easiest experience, use the Streamlit UI!**

```bash
# Make sure all services are running (Qdrant, Inngest, FastAPI)
# Then start the Streamlit UI:
streamlit run streamlit_app.py
```

Open `http://localhost:8501` in your browser. You'll see:
1. **📤 Upload Section**: Drag and drop your PDF file
2. **💬 Chat Interface**: Type your question in natural language
3. **📊 Results**: See the AI's answer with source citations
4. **⚙️ Settings**: Adjust retrieval parameters (top_k)

**No curl commands needed!** Perfect for demos and non-technical users.

---

### API Endpoints

#### 1. Health Check
```bash
curl http://localhost:8000/
```

#### 2. Ingest a PDF

Send an event to ingest a PDF document:

```bash
curl -X POST http://localhost:8288/e/rag_app \
  -H "Content-Type: application/json" \
  -d '{
    "name": "rag/innggest_pdf",
    "data": {
      "pdf_path": "/path/to/your/document.pdf",
      "source": "my-document"
    }
  }'
```

**What happens:**
- 📖 Loads the PDF and splits it into chunks (1000 chars, 200 overlap)
- 🔢 Generates 3072-dimensional embeddings using Gemini
- 💾 Stores vectors in Qdrant with metadata

#### 3. Query the PDF

Ask questions about your ingested documents:

```bash
curl -X POST http://localhost:8288/e/rag_app \
  -H "Content-Type: application/json" \
  -d '{
    "name": "rag/query_pdf_ai",
    "data": {
      "question": "What is the main topic of the document?",
      "top_k": 5
    }
  }'
```

**Response:**
```json
{
  "answer": "The main topic is...",
  "sources": ["my-document"],
  "num_contexts": 5
}
```

**What happens:**
- 🔍 Embeds your question using Gemini
- 📊 Searches Qdrant for the top 5 most relevant chunks
- 🤖 Sends context to Gemini LLM for answer generation
- ✅ Returns the answer with source attribution

### 4. Use the Streamlit UI (Recommended for Easy Testing)

For a user-friendly interface, you can use the Streamlit UI:

```bash
streamlit run streamlit_app.py
```

The UI will open at `http://localhost:8501` and provides:
- 📤 **File Upload**: Drag and drop PDF files to ingest
- 💬 **Chat Interface**: Ask questions naturally
- 📊 **Source Display**: See which document chunks were used
- ⚙️ **Configuration**: Adjust `top_k` and other parameters
- 🎨 **Visual Feedback**: Real-time status updates and loading indicators

**Benefits of the Streamlit UI:**
- No need to write curl commands
- Interactive file upload
- Instant visual feedback
- Better for demos and testing
- User-friendly for non-technical users

### View Workflow Execution

Open the Inngest Dev Server UI at `http://localhost:8288` to see:
- Real-time workflow execution
- Step-by-step logs
- Error tracking
- Execution history
- Retry attempts and failures
- Detailed timing information

## 📁 Project Structure

```
Prodution_Ready_RAG/
├── main.py              # FastAPI app + Inngest functions
├── streamlit_app.py     # Streamlit UI (optional, user-friendly interface)
├── data_loader.py       # PDF loading and embedding logic
├── vector_db.py         # Qdrant vector database wrapper
├── constants.py         # Configuration constants
├── custom_types.py      # Pydantic models
├── .env                 # Environment variables (create this)
├── .gitignore          # Git ignore file
├── pyproject.toml      # Project dependencies
├── README.md           # This file
├── LOGGING_GUIDE.md    # Logging documentation
└── qdrant_storage/     # Qdrant data directory
```

## 🎛️ Configuration

Edit `constants.py` to customize:

```python
# Qdrant
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "docs"

# Embedding
EMBED_MODEL = "gemini-embedding-001"
EMBEDDING_DIM = 3072

# Chunking
CHUNK_SIZE = 1000
OVERLAP = 200

# LLM
GEMINI_LLM_MODEL = "gemini-2.5-flash"
```

## 📊 Logging

The system includes comprehensive logging with emoji indicators:

```
INFO: 📖 Loading PDF: document.pdf
INFO: ✂️ Split into 42 chunks
INFO: 🔢 Embedding 42 chunks...
INFO: ✅ Generated 42 vectors (dim=3072)
INFO: 💾 Upserted 42 vectors to Qdrant
INFO: 🔍 Searching for question: What is RAG?
INFO: ✅ Embedded question into vector of dim=3072
INFO: 📊 Found 5 contexts
INFO: 🎯 Step completed: found 5 contexts from 1 sources
```

See `LOGGING_GUIDE.md` for more details.

## 🔧 Advanced Usage

### Custom Embedding Model

To use a different embedding model:

1. Update `constants.py`:
```python
EMBED_MODEL = "your-model-name"
EMBEDDING_DIM = your_dimension
```

2. Modify `data_loader.py` if needed for different API calls

### Multiple Document Sources

Track different sources by setting the `source` parameter:

```json
{
  "name": "rag/innggest_pdf",
  "data": {
    "pdf_path": "/path/to/doc.pdf",
    "source": "research-papers"
  }
}
```

### Adjust Retrieval

Modify the `top_k` parameter to retrieve more or fewer context chunks:

```json
{
  "name": "rag/query_pdf_ai",
  "data": {
    "question": "Your question?",
    "top_k": 10  // Retrieve top 10 chunks
  }
}
```


## 📚 Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern web framework
- **[Inngest](https://www.inngest.com/)** - Workflow orchestration
- **[Qdrant](https://qdrant.tech/)** - Vector database
- **[Google Gemini](https://ai.google.dev/)** - Embeddings and LLM
- **[LlamaIndex](https://www.llamaindex.ai/)** - PDF parsing and chunking
- **[Streamlit](https://streamlit.io/)** - Interactive web UI
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment management

## 📦 Docker Package

This project is automatically published as a Docker package to GitHub Container Registry (GHCR). The Docker image is built and pushed on every commit to the main branch using GitHub Actions.

### Package Information
- **Registry**: GitHub Container Registry (ghcr.io)
- **Package URL**: https://github.com/faris771/Production-Ready-RAG/pkgs/container/production-ready-rag
- **Public Access**: The package is publicly available for pulling
- **Automated Builds**: Images are automatically built and published via GitHub Actions

### CI/CD Workflow
The `.github/workflows/docker-build.yml` workflow:
- ✅ Builds Docker images on every push to main/master
- ✅ Publishes to GitHub Container Registry automatically
- ✅ Tags images with branch name, commit SHA, and 'latest'
- ✅ Uses GitHub Actions cache for faster builds
- ✅ Includes proper metadata and labels

### Building Locally
To build the Docker image locally:
```bash
docker build -t production-ready-rag:local .
```

To push your own version:
```bash
docker tag production-ready-rag:local ghcr.io/YOUR_USERNAME/production-ready-rag:custom
docker push ghcr.io/YOUR_USERNAME/production-ready-rag:custom
```


