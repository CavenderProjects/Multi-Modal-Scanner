# Project Instructions — Revised Pen Tester

## Core Values
Accuracy and honesty are the most important qualities. Every response should be confirmed as correct before expression to the user.

## Session Start Reminder
At the beginning of every new session, before any other work, remind the user to run the following from `C:\Users\slagb\OneDrive\Documents\Claude\Projects\Revised pen tester`:

```powershell
.\manage.ps1 status
```

And if they are about to push changes:

```powershell
.\manage.ps1 push -Repo scanner    -m "description"   # templates / libraries only
.\manage.ps1 push -Repo standalone -m "description"   # Python scanner only
.\manage.ps1 push -Repo both       -m "description"   # changes that apply to both
```


## Repo Structure
- **Multi-Modal-Scanner** (root): tracks `assets/`, `references/`, `SKILL.md`, `manage.ps1`
- **Multi-Modal-Scanner_Standalone** (at `pen-tester/standalone/`): tracks all `.py` files
- `pen-tester/standalone/` is in the root `.gitignore` — use `manage.ps1` to keep track of which repo is being targeted
