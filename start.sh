#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   Production Ready RAG - Startup      ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ Error: .env file not found!${NC}"
    echo -e "${YELLOW}Please create a .env file with:${NC}"
    echo -e "GEMINI_API_KEY=your_api_key_here"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Found .env file${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python3 found: $(python3 --version)${NC}"

# Check if virtual environment exists, create if not
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source .venv/bin/activate

# Install dependencies
echo -e "${YELLOW}📥 Installing dependencies...${NC}"
pip install -q -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running!${NC}"
    echo -e "${YELLOW}Please start Docker first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker is running${NC}"

# Check if Qdrant is running
echo -e "${YELLOW}🔍 Checking Qdrant...${NC}"
if ! curl -s http://localhost:6333 > /dev/null 2>&1; then
    echo -e "${YELLOW}📦 Starting Qdrant...${NC}"
    docker run -d \
        --name qdrant-rag \
        -p 6333:6333 -p 6334:6334 \
        -v $(pwd)/qdrant_storage:/qdrant/storage:z \
        qdrant/qdrant

    # Wait for Qdrant to start
    echo -e "${YELLOW}⏳ Waiting for Qdrant to start...${NC}"
    sleep 5

    if curl -s http://localhost:6333 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Qdrant started successfully${NC}"
    else
        echo -e "${RED}❌ Failed to start Qdrant${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Qdrant is already running${NC}"
fi

# Check if Inngest is installed
if ! command -v npx &> /dev/null; then
    echo -e "${RED}❌ npx (Node.js) is not installed!${NC}"
    echo -e "${YELLOW}Please install Node.js from https://nodejs.org/${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Node.js found${NC}"

# Start Inngest in background
echo -e "${YELLOW}🚀 Starting Inngest Dev Server...${NC}"
npx inngest-cli@latest dev > inngest.log 2>&1 &
INNGEST_PID=$!
echo $INNGEST_PID > .inngest.pid

# Wait for Inngest to start
sleep 3
echo -e "${GREEN}✅ Inngest Dev Server started (PID: $INNGEST_PID)${NC}"

# Start FastAPI in background
echo -e "${YELLOW}🚀 Starting FastAPI server...${NC}"
uvicorn main:app --reload --log-level info > fastapi.log 2>&1 &
FASTAPI_PID=$!
echo $FASTAPI_PID > .fastapi.pid

# Wait for FastAPI to start
sleep 3
echo -e "${GREEN}✅ FastAPI started (PID: $FASTAPI_PID)${NC}"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ All services started successfully!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}📍 Service URLs:${NC}"
echo -e "   FastAPI:        ${BLUE}http://localhost:8000${NC}"
echo -e "   Inngest:        ${BLUE}http://localhost:8288${NC}"
echo -e "   Qdrant:         ${BLUE}http://localhost:6333${NC}"
echo ""
echo -e "${YELLOW}📝 To start Streamlit UI:${NC}"
echo -e "   ${GREEN}streamlit run streamlit_app.py${NC}"
echo ""
echo -e "${YELLOW}📋 Logs:${NC}"
echo -e "   FastAPI:  tail -f fastapi.log"
echo -e "   Inngest:  tail -f inngest.log"
echo ""
echo -e "${YELLOW}🛑 To stop all services:${NC}"
echo -e "   ${GREEN}./stop.sh${NC}"
echo ""

