# AI Agent Collaboration

This file documents the collaboration between multiple AI agents working on different aspects of the project.

## Agent Responsibilities

- **AI-1**: [To be defined - specific responsibilities]
- **AI-2**: [To be defined - specific responsibilities] 
- **AI-3**: [To be defined - specific responsibilities]

## Coordination Protocol

1. Each agent works in their dedicated branch (ai-1, ai-2, ai-3)
2. Regular sync points to merge non-conflicting changes
3. Conflict resolution protocol when changes overlap
4. Testing requirements before merging to dev branch
5. Documentation updates in this file as needed

## Merge Workflow

1. Agent completes work in their branch
2. Pull latest dev to check for conflicts
3. Resolve any conflicts
4. Test changes
5. Push to dev branch
6. Update this document with work summary

## Status Tracking

- Last sync: [Date]
- Active agents: [List active agents]
- Current issues: [Any known conflicts or blockers]
- Next sync: [Date]

## Git Pull and Merge Instructions for Local Repository

### Setting Upstream Branches
To set the upstream branch for your local branch:
```
git branch --set-upstream-to=origin/<remote_branch_name> <local_branch_name>
```

For example, to make ai-1 track the dev branch:
```
git branch --set-upstream-to=origin/dev ai-1
```

### Pull Script for Dev Branch
A helper script is available to synchronize your current branch with the dev branch:
```
./pull.sh
```

This script detects which branch you're on and performs the appropriate actions:
- If on the dev branch: pulls from origin/dev
- If on any other branch (like ai-1, ai-2, ai-3): merges from origin/dev and pushes to the current branch

### Checking Current Worktree
Before starting work, always verify which worktree and branch you're in:
```
pwd
git branch
```

This helps avoid accidental work on the wrong branch.

### Git Pull

To pull the latest changes from the remote repository:
```
git pull
```
This command fetches and merges changes from the remote branch that your current branch is tracking.

To pull from a specific remote and branch:
```
git pull origin branch_name
```

To fetch changes first, then merge them manually (more control):
```
git fetch
git merge origin/main  # or whatever the remote branch is named
```

### Git Merge

To merge another branch into your current branch:
```
git checkout main          # switch to the branch you want to merge into
git merge branch_to_merge  # merge the other branch into current branch
```

To create a merge commit even for fast-forward merges:
```
git merge --no-ff branch_name
```

To merge with a log of what commits were merged:
```
git merge --log branch_name
```

### Handling Merge Conflicts

To identify files with conflicts:
```
git status
```

To resolve conflicts:
1. Edit the conflicted files to resolve differences (look for conflict markers `<<<<<<<`, `=======`, `>>>>>>>`)
2. Stage the resolved files:
   ```
   git add file_name
   ```
3. Complete the merge with a commit:
   ```
   git commit
   ```

To abort a merge if needed:
```
git merge --abort
```

### Git Pull vs. Git Fetch + Merge

- `git pull` = `git fetch` + `git merge`
- `git fetch` alone allows you to see what changes are available before merging
- Use `git fetch` + `git merge` for more control over the merge process

### Best Practices

1. Always run tests after pulling to ensure nothing broke
2. Commit your changes before pulling to avoid losing uncommitted work
3. Use `git status` frequently to understand your repository state
4. Resolve conflicts immediately when they occur
5. Keep a clean, understandable commit history
6. Verify your current worktree/branch before starting work
7. Use `git worktree list` to see all active worktrees
8. Use `./pull.sh` script when pulling from dev branch for consistency
