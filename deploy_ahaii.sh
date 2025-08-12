#!/bin/bash

# AHAII Deployment Script
# Based on TAIFA-FIALA deployment pattern but using separate directories
# to avoid conflicts with existing TAIFA deployment

set -e

echo "🏥 AHAII (African Health AI Infrastructure Index) Deployment"
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SERVER_USER="jforrest"
SERVER_HOST="100.75.201.24" 
SERVER_PATH="~/production/ahaii"  # Different from TAIFA path
BACKEND_PORT="8030" 
FRONTEND_PORT="3030"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}
print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "CLAUDE.md" ]; then
    print_error "This script should be run from the AHAII project root directory"
    exit 1
fi

print_status "Building frontend..."
cd frontend
npm install
npm run build
cd ..

print_status "Preparing backend..."
cd backend
# Use Python 3.12 compatible requirements
if [ -f "../requirements-python312.txt" ]; then
    pip install -r ../requirements-python312.txt
else
    pip install -r requirements.txt
fi
cd ..

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Sync latest changes from local to production (including frontend build)
print_status "📤 Syncing local changes to production..."
rsync -avz -e "ssh -o Ciphers=aes256-gcm@openssh.com" --exclude='.git' --exclude='node_modules' --exclude='venv' --exclude='logs' --exclude='*.log' --exclude='__pycache__' --exclude='*.pyc' --exclude='.env.local' --exclude='.env' "$SCRIPT_DIR/" ${SERVER_USER}@${SERVER_HOST}:${SERVER_PATH}/

# Separately copy .env file securely
print_status "Copying production .env file..."
if [ -f ".env" ]; then
    scp -o Ciphers=aes256-gcm@openssh.com .env ${SERVER_USER}@${SERVER_HOST}:${SERVER_PATH}/.env
    print_status "✓ .env file copied to production"
else
    print_warning "⚠ No .env file found - make sure to set up environment variables on the server"
fi

print_status "Setting up production environment and restarting services..."
ssh ${SERVER_USER}@${SERVER_HOST} "
    cd ${SERVER_PATH}
    
    # Unlock keychain for production operations
    echo 'Unlocking keychain for production deployment...'
    if ! security unlock-keychain -p \"\$(security find-generic-password -w -s 'keychain-unlock' -a \$USER)\" ~/Library/Keychains/login.keychain-db 2>/dev/null; then
        echo '⚠ Keychain unlock failed - some operations may not work'
    fi
    
    # Set production environment
    export ENVIRONMENT=production
    export DEBUG=false
    export LOG_LEVEL=INFO
    
    # Stop existing AHAII services and clear ports
    echo 'Stopping existing AHAII services and clearing ports...'
    
    # Kill processes by name pattern
    pkill -f 'uvicorn.*${BACKEND_PORT}' || true
    pkill -f 'npm.*${FRONTEND_PORT}' || true
    pkill -f 'next.*${FRONTEND_PORT}' || true
    
    # Force kill any processes using our ports
    echo 'Clearing port ${BACKEND_PORT} (backend)...'
    lsof -ti:${BACKEND_PORT} | xargs kill -9 2>/dev/null || echo 'Port ${BACKEND_PORT} is free'
    
    echo 'Clearing port ${FRONTEND_PORT} (frontend)...'
    lsof -ti:${FRONTEND_PORT} | xargs kill -9 2>/dev/null || echo 'Port ${FRONTEND_PORT} is free'
    
    # Wait a moment for ports to clear
    sleep 2
    
    # Verify ports are free
    if lsof -i:${BACKEND_PORT} >/dev/null 2>&1; then
        echo '⚠ Warning: Port ${BACKEND_PORT} still in use'
        lsof -i:${BACKEND_PORT}
    else
        echo '✓ Port ${BACKEND_PORT} is available'
    fi
    
    if lsof -i:${FRONTEND_PORT} >/dev/null 2>&1; then
        echo '⚠ Warning: Port ${FRONTEND_PORT} still in use'
        lsof -i:${FRONTEND_PORT}
    else
        echo '✓ Port ${FRONTEND_PORT} is available'
    fi
    
    # Install/update backend dependencies  
    echo 'Setting up backend environment...'
    cd backend
    python3 -m venv venv 2>/dev/null || true
    source venv/bin/activate
    
    # Use Python 3.12 compatible requirements
    if [ -f "../requirements-python312.txt" ]; then
        echo 'Using Python 3.12 compatible requirements...'
        pip install -r ../requirements-python312.txt
    else
        echo 'Using standard requirements...'
        pip install -r requirements.txt
    fi
    
    # Start backend service
    echo 'Starting AHAII backend on port ${BACKEND_PORT}...'
    nohup python -m uvicorn main:app --host 0.0.0.0 --port ${BACKEND_PORT} > ../ahaii_backend.log 2>&1 &
    
    # Setup and start frontend
    echo 'Setting up frontend environment...'
    cd ../frontend
    
    # Load nvm to ensure npm is available
    export NVM_DIR="\$HOME/.nvm"
    [ -s "\$NVM_DIR/nvm.sh" ] && source "\$NVM_DIR/nvm.sh"
    nvm use default
    
    # Create production .env.local for frontend
    echo 'Setting up production frontend environment variables...'
    cat > .env.local << EOF
# Frontend .env.local for AHAII Project - Production

# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://wkhrjnuvncczofzgfmqe.supabase.co
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY=sb_publishable_dG_AEhs9r_pbO8XjbpSAkw_wlvPFkyk

# Production API Configuration
NEXT_PUBLIC_API_URL=https://api.taifa-fiala.net
EOF
    
    npm install --production
    
    # Build frontend on server with production settings
    echo 'Building frontend for production...'
    npm run build
    
    # Start frontend service  
    echo 'Starting AHAII frontend on port ${FRONTEND_PORT}...'
    nohup npm run start -- -p ${FRONTEND_PORT} > ../ahaii_frontend.log 2>&1 &
    
    echo 'AHAII services started:'
    echo '  - Backend: http://localhost:${BACKEND_PORT}'
    echo '  - Frontend: http://localhost:${FRONTEND_PORT}'
    echo '  - Logs: ahaii_backend.log, ahaii_frontend.log'
"

print_status "AHAII has been deployed to production server!"
print_status "AHAII is using:"
print_status "  - Server path: ${SERVER_PATH} (separate from TAIFA)"
print_status "  - Backend port: ${BACKEND_PORT}"
print_status "  - Frontend port: ${FRONTEND_PORT}"

# Clean up
print_status "Cleaning up temporary files..."
rm -rf deploy_temp

print_status "🎉 AHAII deployment complete!"
