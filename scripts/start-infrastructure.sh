#!/bin/bash

# Multi-Agent RAG System Infrastructure Startup Script

set -e

echo "🚀 Starting Multi-Agent RAG System Infrastructure..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before running again."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p airflow/logs
mkdir -p airflow/plugins
mkdir -p uploads

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Check service health
echo "🏥 Checking service health..."

services=("rag-postgres" "rag-redis" "rag-opensearch")
for service in "${services[@]}"; do
    echo "Checking $service..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if docker-compose ps | grep "$service" | grep -q "healthy"; then
            echo "✅ $service is healthy"
            break
        fi
        sleep 2
        timeout=$((timeout-2))
    done
    
    if [ $timeout -le 0 ]; then
        echo "❌ $service failed to become healthy"
        docker-compose logs "$service"
        exit 1
    fi
done

echo "🎉 Infrastructure started successfully!"
echo ""
echo "📊 Service URLs:"
echo "  • API: http://localhost:8000"
echo "  • API Docs: http://localhost:8000/docs"
echo "  • Airflow: http://localhost:8080 (admin/admin)"
echo "  • OpenSearch Dashboards: http://localhost:5601"
echo "  • Langfuse: http://localhost:3000"
echo "  • Ollama: http://localhost:11434"
echo ""
echo "🔍 To check logs: docker-compose logs -f [service-name]"
echo "🛑 To stop: docker-compose down"
echo "🗑️  To clean up: docker-compose down -v"