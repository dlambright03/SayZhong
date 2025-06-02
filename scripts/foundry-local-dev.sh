#!/bin/bash

# Azure AI Foundry Local Management Script for SayZhong Dev Container
# This script helps manage the optional AI testing sidecar container

set -e

COMPOSE_FILE="/workspaces/SayZhong/.devcontainer/docker-compose.ai-testing.yml"
PROFILE="ai-testing"
CONTAINER_NAME="sayzhong-foundry-local"

show_usage() {
    echo "Usage: $0 [start|stop|status|logs|restart]"
    echo ""
    echo "Commands:"
    echo "  start   - Start AI testing sidecar (downloads model if needed)"
    echo "  stop    - Stop AI testing sidecar and free resources"
    echo "  status  - Show container status and resource usage"
    echo "  logs    - Show container logs (useful during startup)"
    echo "  restart - Restart the container (useful if stuck)"
    echo ""
    echo "Examples:"
    echo "  $0 start    # Start AI testing mode"
    echo "  $0 logs     # Monitor startup progress"
    echo "  $0 stop     # Stop to save resources"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker not found. Please ensure Docker is available in the dev container."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose not found. Please ensure Docker Compose is available."
        exit 1
    fi
}

start_ai_testing() {
    echo "🚀 Starting Azure AI Foundry Local for AI testing..."
    echo "⚠️  This will use ~8GB RAM and may take 5-10 minutes for initial model download."
    echo ""
    
    docker-compose -f "$COMPOSE_FILE" --profile "$PROFILE" up -d foundry-local
    
    echo "✅ Container started. Monitoring startup progress..."
    echo "💡 Use '$0 logs' to monitor detailed progress"
    echo "💡 Use '$0 status' to check resource usage"
    echo ""
    
    # Show initial logs
    docker-compose -f "$COMPOSE_FILE" logs --tail=10 foundry-local
}

stop_ai_testing() {
    echo "🛑 Stopping Azure AI Foundry Local..."
    
    docker-compose -f "$COMPOSE_FILE" --profile "$PROFILE" down
    
    echo "✅ AI testing mode stopped. Resources freed."
    echo "💡 Models are cached and will start faster next time."
}

show_status() {
    echo "📊 Azure AI Foundry Local Status"
    echo "================================="
    
    if docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -q "$CONTAINER_NAME"; then
        echo "✅ Status: Running"
        echo ""
        echo "🔗 Endpoints:"
        echo "   - API: http://localhost:8080"
        echo "   - Management: http://localhost:8081"
        echo ""
        echo "📈 Resource Usage:"
        docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}" "$CONTAINER_NAME" 2>/dev/null || echo "   Unable to get stats"
        echo ""
        echo "🏥 Health Status:"
        docker inspect "$CONTAINER_NAME" --format='   {{.State.Health.Status}}' 2>/dev/null || echo "   Health check not available"
    else
        echo "❌ Status: Not running"
        echo ""
        echo "💡 Use '$0 start' to begin AI testing mode"
    fi
}

show_logs() {
    echo "📝 Azure AI Foundry Local Logs"
    echo "==============================="
    echo "💡 Press Ctrl+C to stop following logs"
    echo ""
    
    if docker ps --format "{{.Names}}" | grep -q "$CONTAINER_NAME"; then
        docker-compose -f "$COMPOSE_FILE" logs -f foundry-local
    else
        echo "❌ Container not running. Use '$0 start' first."
        exit 1
    fi
}

restart_ai_testing() {
    echo "🔄 Restarting Azure AI Foundry Local..."
    
    stop_ai_testing
    sleep 2
    start_ai_testing
}

main() {
    check_docker
    
    case "${1:-}" in
        "start")
            start_ai_testing
            ;;
        "stop")
            stop_ai_testing
            ;;
        "status")
            show_status
            ;;
        "logs")
            show_logs
            ;;
        "restart")
            restart_ai_testing
            ;;
        "help"|"-h"|"--help")
            show_usage
            ;;
        "")
            echo "❌ No command specified."
            echo ""
            show_usage
            exit 1
            ;;
        *)
            echo "❌ Unknown command: $1"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

main "$@"
