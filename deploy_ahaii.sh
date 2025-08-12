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
SERVER_USER="your-server-user"
SERVER_HOST="your-server-host" 
SERVER_PATH="/var/www/ahaii"  # Different from TAIFA path
BACKEND_PORT="8031"  # Different from TAIFA port (8030)
FRONTEND_PORT="3031"  # Different from TAIFA port (3030)

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
pip install -r requirements.txt
cd ..

print_status "Creating deployment package..."
# Create a deployment directory
mkdir -p deploy_temp
mkdir -p deploy_temp/frontend
mkdir -p deploy_temp/backend

# Copy frontend build
cp -r frontend/build/* deploy_temp/frontend/ 2>/dev/null || cp -r frontend/out/* deploy_temp/frontend/ 2>/dev/null || cp -r frontend/.next/* deploy_temp/frontend/

# Copy backend files
cp -r backend/* deploy_temp/backend/
cp requirements.txt deploy_temp/ 2>/dev/null || true

# Copy configuration files
cp CLAUDE.md deploy_temp/
cp database/ahaii_schema.sql deploy_temp/ 2>/dev/null || true

print_status "Deployment package ready in deploy_temp/"

# If you have server credentials configured, uncomment and modify these lines:
# print_status "Syncing to server (avoiding TAIFA directory)..."
# rsync -avz --delete deploy_temp/ ${SERVER_USER}@${SERVER_HOST}:${SERVER_PATH}/
# 
# print_status "Restarting services on server..."
# ssh ${SERVER_USER}@${SERVER_HOST} "
#     cd ${SERVER_PATH}
#     
#     # Stop existing AHAII services (not TAIFA)
#     pkill -f 'uvicorn.*8031' || true
#     pkill -f 'npm.*3031' || true
#     
#     # Start backend on port ${BACKEND_PORT}
#     cd backend && nohup python -m uvicorn main:app --host 0.0.0.0 --port ${BACKEND_PORT} > ../ahaii_backend.log 2>&1 &
#     
#     # Start frontend on port ${FRONTEND_PORT} 
#     cd ../frontend && nohup npm start -- -p ${FRONTEND_PORT} > ../ahaii_frontend.log 2>&1 &
#     
#     echo 'AHAII services started on ports ${BACKEND_PORT} and ${FRONTEND_PORT}'
# "

print_warning "Server deployment commands are commented out for safety."
print_warning "Please configure SERVER_USER, SERVER_HOST, and SERVER_PATH variables"
print_warning "and uncomment the deployment section before using for production."

print_status "Local deployment package complete!"
print_status "AHAII will use:"
print_status "  - Server path: ${SERVER_PATH} (separate from TAIFA)"
print_status "  - Backend port: ${BACKEND_PORT}"
print_status "  - Frontend port: ${FRONTEND_PORT}"
print_status ""
print_status "To deploy manually:"
print_status "  1. Configure server details in this script"
print_status "  2. Uncomment the server deployment section"
print_status "  3. Run: ./deploy_ahaii.sh"

# Clean up
print_status "Cleaning up temporary files..."
rm -rf deploy_temp

print_status "🎉 AHAII deployment preparation complete!"