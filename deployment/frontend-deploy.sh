#!/bin/bash

# Frontend Deployment Script

echo "Starting frontend deployment..."

# Variables
FRONTEND_DIR="./frontend"
BUILD_DIR="$FRONTEND_DIR/build"
SERVER_USER="ml6user"
SERVER_HOST="your_frontend_server_ip"
SERVER_PATH="/var/www/html/food-ordering-app"

# 1. Navigate to frontend directory
cd $FRONTEND_DIR

# 2. Install dependencies
echo "Installing frontend dependencies..."
npm install

# 3. Build the React application
echo "Building frontend application..."
npm run build

# Check if build was successful
if [ $? -ne 0 ]; then
    echo "Frontend build failed. Exiting."
    exit 1
fi

echo "Frontend build successful. Copying files to server..."

# 4. Rsync build directory to the production server
#    -a: archive mode (preserves permissions, etc.)
#    -v: verbose
#    -z: compress file data during the transfer
#    --delete: delete extraneous files from dest dir (not in src)
rsync -avz --delete $BUILD_DIR/ $SERVER_USER@$SERVER_HOST:$SERVER_PATH

# Check if rsync was successful
if [ $? -ne 0 ]; then
    echo "Frontend deployment failed during rsync. Exiting."
    exit 1
fi

echo "Frontend deployment completed successfully!"

# Optional: Invalidate CDN cache if applicable
# echo "Invalidating CDN cache..."
# aws cloudfront create-invalidation --distribution-id YOUR_CLOUDFRONT_DISTRIBUTION_ID --paths "/*"
