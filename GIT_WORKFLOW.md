# Git Workflow Guide

> Personal reference for managing this project with Git and GitHub.

---

## Branch Structure

```
main   ← stable, working app (ready to use)
dev    ← new features in progress
```

**Rule: `main` must always run without errors.**
Never commit broken code to `main`. Experiment on `dev`, merge to `main` only when tested and working.

---

## Daily Workflow

### 1. Working on a New Feature

```bash
# Start from dev
git checkout dev
git pull origin dev

# Make changes, then save progress
git add .
git commit -m "add: beam deflection calculator input form"

# Push to GitHub
git push origin dev
```

### 2. Feature is Done — Release to Main

```bash
git checkout main
git merge dev
git push origin main
```

---

## Commit Message Convention

Format: `<prefix>: short description of what changed`

| Prefix | Use for |
|--------|---------|
| `add:` | New feature or file |
| `fix:` | Bug fix |
| `update:` | Improvement to existing feature |
| `remove:` | Deleted something |

**Examples:**
```
add: wind load calculator for flat roof
fix: wrong moment of inertia formula for I-beam
update: improve input validation for beam span
remove: unused dead load table
```

---

## Optional: Feature Branches (for bigger experiments)

When working on something large or risky, branch off `dev` instead of committing directly to it.

```bash
# Create a feature branch from dev
git checkout dev
git checkout -b feature/wind-load-calculator

# Work on it...
git add .
git commit -m "add: wind load calculator draft"

# When done, merge back to dev
git checkout dev
git merge feature/wind-load-calculator

# Clean up
git branch -d feature/wind-load-calculator
```

Use this when you want to keep `dev` clean while experimenting with multiple things at once.

---

## Weekly Habit

| Step | Action |
|------|--------|
| Start work | `git checkout dev` |
| During work | `git commit` often — small saves are better than one big one |
| Feature done & tested | Merge `dev` → `main` |
| Before closing | `git push` both branches to GitHub |

---

## Quick Reference — Common Commands

```bash
# Check current status
git status

# See commit history
git log --oneline

# Switch branch
git checkout <branch-name>

# Create and switch to new branch
git checkout -b <branch-name>

# Stage all changes
git add .

# Commit with message
git commit -m "your message here"

# Push to GitHub
git push origin <branch-name>

# Merge a branch into current branch
git merge <branch-name>

# Pull latest from GitHub
git pull origin <branch-name>
```

---

## Branch Diagram

```
main  ─────●─────────────────────●─────────────────────●
            \                   /                       /
dev          ●───●───●─────────●───●───●───●───●──────
                               ^                       ^
                          merge to main           merge to main
                         (milestone done)        (milestone done)
```

Treat each project milestone (e.g. *"this version can design a simply supported beam"*) as a `dev → main` merge event.