#!/bin/bash

# Backend Deployment Script

echo "Starting backend deployment..."

# Variables
BACKEND_DIR="./backend"
SERVER_USER="ml6user"
SERVER_HOST="your_backend_server_ip"
SERVER_PATH="/opt/food-ordering-api"
SERVICE_NAME="food-ordering-api"

# 1. Navigate to backend directory
cd $BACKEND_DIR

# 2. Install dependencies
echo "Installing backend dependencies..."
npm install --production

# Check if install was successful
if [ $? -ne 0 ]; then
    echo "Backend dependency installation failed. Exiting."
    exit 1
fi

echo "Backend dependencies installed. Copying files to server..."

# 3. Rsync backend directory to the production server
rsync -avz --exclude='node_modules' --exclude='tests' --delete ./ $SERVER_USER@$SERVER_HOST:$SERVER_PATH

# Check if rsync was successful
if [ $? -ne 0 ]; then
    echo "Backend deployment failed during rsync. Exiting."
    exit 1
fi

echo "Backend files copied. Restarting backend service..."

# 4. SSH into the server and restart the service
ssh $SERVER_USER@$SERVER_HOST << EOF
  echo "Navigating to backend path on server..."
  cd $SERVER_PATH

  echo "Installing production dependencies on server..."
  npm install --production

  echo "Restarting $SERVICE_NAME service..."
  sudo systemctl restart $SERVICE_NAME
  sudo systemctl status $SERVICE_NAME --no-pager
EOF

# Check if SSH command was successful
if [ $? -ne 0 ]; then
    echo "Backend service restart failed. Exiting."
    exit 1
fi

echo "Backend deployment completed successfully!"
