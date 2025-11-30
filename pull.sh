#!/bin/bash

# Script to pull the latest changes from the dev branch and push to the current branch
# This script pulls from dev and pushes to the current branch depending on which worktree it's used in

echo "Synchronizing with dev branch and pushing to current branch..."

# Check current directory to ensure we're in the right place
if [ -d ".git" ] || git rev-parse --git-dir > /dev/null 2>&1; then
    CURRENT_BRANCH=$(git branch --show-current)

    echo "Current branch detected: $CURRENT_BRANCH"

    if [ "$CURRENT_BRANCH" = "dev" ]; then
        # If on dev branch, pull from dev
        git pull origin dev
        echo "Successfully pulled latest changes from dev branch"
    else
        # If on any other branch (like ai-1, ai-2, ai-3), pull from dev and push to current branch
        echo "Pulling latest changes from dev branch to $CURRENT_BRANCH..."
        git merge origin/dev
        echo "Pushing current branch $CURRENT_BRANCH to remote..."
        git push origin $CURRENT_BRANCH
    fi
else
    echo "Error: Not in a git repository"
    exit 1
fi