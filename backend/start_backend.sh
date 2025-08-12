#!/bin/bash

# AHAII Backend Startup Script
# African Health AI Infrastructure Index - API Server

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$SCRIPT_DIR"

# Default configuration
DEFAULT_HOST="0.0.0.0"
DEFAULT_PORT="8000"
DEFAULT_ENVIRONMENT="development"

# Parse command line arguments
ENVIRONMENT="${1:-$DEFAULT_ENVIRONMENT}"
HOST="${2:-$DEFAULT_HOST}"
PORT="${3:-$DEFAULT_PORT}"

print_banner() {
    echo -e "${CYAN}"
    echo "=================================================================="
    echo "               AHAII Backend API Server"
    echo "     African Health AI Infrastructure Index"
    echo "=================================================================="
    echo -e "${NC}"
}

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

check_requirements() {
    print_info "Checking system requirements..."
    
    # Check if we're in the right directory
    if [ ! -f "$BACKEND_DIR/main.py" ]; then
        print_error "main.py not found. Please run this script from the backend directory."
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 is not installed or not in PATH"
        exit 1
    fi
    
    # Check pip
    if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
        print_error "pip is not installed or not in PATH"
        exit 1
    fi
    
    print_status "System requirements check passed"
}

setup_environment() {
    print_info "Setting up Python environment..."
    
    # Change to backend directory
    cd "$BACKEND_DIR"
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_info "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    print_status "Virtual environment activated"
    
    # Check if requirements.txt exists
    if [ -f "requirements.txt" ]; then
        print_info "Installing dependencies from requirements.txt..."
        pip install -r requirements.txt
    else
        print_warning "No requirements.txt found. Installing essential packages..."
        pip install fastapi uvicorn python-multipart supabase loguru python-dotenv
    fi
    
    print_status "Dependencies installed"
}

check_environment_variables() {
    print_info "Checking environment variables..."
    
    # Check for .env file
    if [ -f "$BACKEND_DIR/.env" ]; then
        print_status "Found .env file"
        export $(cat "$BACKEND_DIR/.env" | grep -v '^#' | xargs)
    else
        print_warning "No .env file found. Please ensure environment variables are set."
    fi
    
    # Check critical environment variables
    if [ -z "$SUPABASE_URL" ] && [ -z "$DATABASE_URL" ]; then
        print_warning "Database connection variables not found. API may not function properly."
    fi
    
    print_status "Environment variables checked"
}

test_database_connection() {
    print_info "Testing database connection..."
    
    # Simple Python script to test connection
    python3 -c "
import sys
sys.path.append('$BACKEND_DIR')

try:
    from config.database import supabase
    response = supabase.table('countries').select('id').limit(1).execute()
    if response.data is not None:
        print('✅ Database connection successful')
    else:
        print('⚠️  Database connection failed')
        sys.exit(1)
except Exception as e:
    print(f'❌ Database connection error: {str(e)}')
    sys.exit(1)
" || {
        print_warning "Database connection test failed. Server will start but may not function properly."
    }
}

start_server() {
    print_info "Starting AHAII Backend API Server..."
    print_info "Environment: $ENVIRONMENT"
    print_info "Host: $HOST"
    print_info "Port: $PORT"
    print_info "Backend Directory: $BACKEND_DIR"
    
    echo -e "${PURPLE}"
    echo "=================================================================="
    echo "🚀 Server Starting..."
    echo "📍 API Documentation: http://$HOST:$PORT/docs"
    echo "🔍 Health Check: http://$HOST:$PORT/health"
    echo "🌍 Countries API: http://$HOST:$PORT/api/countries/"
    echo "=================================================================="
    echo -e "${NC}"
    
    # Set environment variables
    export ENVIRONMENT="$ENVIRONMENT"
    export HOST="$HOST"
    export PORT="$PORT"
    
    # Start the server
    if [ "$ENVIRONMENT" == "development" ]; then
        # Development mode with auto-reload
        uvicorn main:app --host "$HOST" --port "$PORT" --reload --log-level info
    elif [ "$ENVIRONMENT" == "production" ]; then
        # Production mode
        uvicorn main:app --host "$HOST" --port "$PORT" --workers 4 --log-level warning
    else
        # Default mode
        uvicorn main:app --host "$HOST" --port "$PORT" --log-level info
    fi
}

cleanup() {
    print_info "Shutting down server..."
    # Kill any remaining uvicorn processes
    pkill -f "uvicorn.*main:app" 2>/dev/null || true
    print_status "Server shutdown complete"
}

show_help() {
    echo "AHAII Backend Startup Script"
    echo ""
    echo "Usage: $0 [ENVIRONMENT] [HOST] [PORT]"
    echo ""
    echo "Arguments:"
    echo "  ENVIRONMENT    Server environment (development|production|staging) [default: development]"
    echo "  HOST          Host to bind to [default: 0.0.0.0]"
    echo "  PORT          Port to bind to [default: 8000]"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Start in development mode on 0.0.0.0:8000"
    echo "  $0 production                         # Start in production mode"
    echo "  $0 development localhost 8080         # Start on localhost:8080"
    echo ""
    echo "Environment Variables:"
    echo "  SUPABASE_URL        Supabase project URL"
    echo "  SUPABASE_ANON_KEY   Supabase anonymous key"
    echo "  DATABASE_URL        Alternative database URL"
    echo "  ENVIRONMENT         Override environment setting"
    echo ""
    echo "Available Endpoints:"
    echo "  /                   API information"
    echo "  /health             Health check"
    echo "  /docs               Interactive API documentation"
    echo "  /api/countries/     Countries API endpoints"
    echo ""
}

# Handle command line options
case "$1" in
    -h|--help)
        show_help
        exit 0
        ;;
esac

# Set up signal handlers
trap cleanup EXIT INT TERM

# Main execution
main() {
    print_banner
    check_requirements
    setup_environment
    check_environment_variables
    test_database_connection
    start_server
}

# Run main function
main
