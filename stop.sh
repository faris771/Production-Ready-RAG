#!/bin/bash
echo -e "${GREEN}✅ All services stopped${NC}"

fi
    echo -e "${GREEN}✅ Qdrant stopped${NC}"
    docker rm qdrant-rag > /dev/null 2>&1
    docker stop qdrant-rag > /dev/null 2>&1
if docker ps | grep -q qdrant-rag; then
# Stop Qdrant

fi
    rm .inngest.pid
    fi
        echo -e "${GREEN}✅ Inngest stopped${NC}"
        kill $INNGEST_PID
    if ps -p $INNGEST_PID > /dev/null 2>&1; then
    INNGEST_PID=$(cat .inngest.pid)
if [ -f .inngest.pid ]; then
# Stop Inngest

fi
    rm .fastapi.pid
    fi
        echo -e "${GREEN}✅ FastAPI stopped${NC}"
        kill $FASTAPI_PID
    if ps -p $FASTAPI_PID > /dev/null 2>&1; then
    FASTAPI_PID=$(cat .fastapi.pid)
if [ -f .fastapi.pid ]; then
# Stop FastAPI

echo -e "${YELLOW}🛑 Stopping all services...${NC}"

NC='\033[0m' # No Color
YELLOW='\033[1;33m'
RED='\033[0;31m'
GREEN='\033[0;32m'
# Colors for output


