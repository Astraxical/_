#!/bin/bash

# Script to pull the latest changes from the dev branch
# This script should be run from within the dev branch worktree

echo "Pulling latest changes from dev branch..."

# Check current directory to ensure we're in the right place
if [ -d ".git" ] || git rev-parse --git-dir > /dev/null 2>&1; then
    CURRENT_BRANCH=$(git branch --show-current)
    
    if [ "$CURRENT_BRANCH" = "dev" ]; then
        git pull origin dev
        echo "Successfully pulled latest changes from dev branch"
    else
        echo "Error: This script should be run from the dev branch"
        echo "Current branch is: $CURRENT_BRANCH"
        exit 1
    fi
else
    echo "Error: Not in a git repository"
    exit 1
fi