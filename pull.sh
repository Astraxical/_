#!/bin/bash

# Script to pull the latest changes from the dev branch in an individual repository
# This script updates the current dev branch with changes from origin

echo "Synchronizing dev branch with remote..."

# Check current directory to ensure we're in the right place
if [ -d ".git" ] || git rev-parse --git-dir > /dev/null 2>&1; then
    CURRENT_BRANCH=$(git branch --show-current)
    
    echo "Current branch detected: $CURRENT_BRANCH"
    
    # Pull the latest changes from origin/dev
    git pull origin dev
    echo "Successfully pulled latest changes from origin/dev"
else
    echo "Error: Not in a git repository"
    exit 1
fi