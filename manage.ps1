# manage.ps1 — Git management for the pen-tester project
#
# USAGE:
#   .\manage.ps1 status                          # show both repos
#   .\manage.ps1 push -Repo scanner    -m "msg"  # push Multi-Modal-Scanner
#   .\manage.ps1 push -Repo standalone -m "msg"  # push Standalone Python scanner
#   .\manage.ps1 push -Repo both       -m "msg"  # push both
#
# FILE OWNERSHIP (which repo tracks what):
#
#   Multi-Modal-Scanner (Claude-based scanner)
#     pen-tester/assets/*.html          — report templates
#     pen-tester/references/*.md        — control libraries
#     pen-tester/SKILL.md               — Claude agent skill definition
#
#   Multi-Modal-Scanner_Standalone (Python scanner)
#     pen-tester/standalone/*.py        — scanner engine, reporter, controls parser
#     pen-tester/standalone/gui/        — desktop GUI
#
#   SHARED CONCERN (changes may apply to both):
#     standalone/controls.py            — parser logic affects template output
#     references/*.md                   — read at runtime by Standalone; tracked
#                                         in Multi-Modal-Scanner only. Standalone
#                                         reads from the local filesystem so local
#                                         changes are always available, but the
#                                         Standalone GitHub repo won't have them.

param(
    [Parameter(Position=0)]
    [ValidateSet("status","push")]
    [string]$Command = "status",

    [ValidateSet("scanner","standalone","both")]
    [string]$Repo,

    [string]$m
)

$ROOT       = Split-Path -Parent $MyInvocation.MyCommand.Path
$STANDALONE = "$ROOT\pen-tester\standalone"

# ── Helpers ───────────────────────────────────────────────────────────────────

function Show-RepoStatus {
    param([string]$Label, [string]$Color, [string]$Path)
    $width = 44
    $bar   = "═" * $width
    Write-Host "`n╔$bar╗" -ForegroundColor $Color
    $pad = " " * [Math]::Max(0, $width - $Label.Length)
    Write-Host "║  $Label$pad║" -ForegroundColor $Color
    Write-Host "╚$bar╝" -ForegroundColor $Color
    Push-Location $Path
    $status = git status --short 2>&1
    if ($status) {
        Write-Host $status
    } else {
        Write-Host "  (nothing to commit, working tree clean)" -ForegroundColor DarkGray
    }
    Write-Host "  Recent commits:" -ForegroundColor DarkGray
    git log --oneline -3 2>&1 | ForEach-Object { Write-Host "  $_" -ForegroundColor DarkGray }
    Pop-Location
}

function Invoke-Push {
    param([string]$Label, [string]$Color, [string]$Path, [string]$Message)
    Write-Host "`n[$Label] Staging and committing..." -ForegroundColor $Color
    Push-Location $Path
    git add -A
    $result = git commit -m $Message 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host $result -ForegroundColor $Color
        Write-Host "[$Label] Pushing..." -ForegroundColor $Color
        git push 2>&1 | ForEach-Object { Write-Host $_ }
        Write-Host "[$Label] Done." -ForegroundColor Green
    } else {
        Write-Host $result -ForegroundColor DarkGray
        Write-Host "[$Label] Nothing new to push." -ForegroundColor DarkGray
    }
    Pop-Location
}

# ── Commands ──────────────────────────────────────────────────────────────────

switch ($Command) {

    "status" {
        Show-RepoStatus "Multi-Modal-Scanner  (Claude / templates / libraries)" "Cyan"   $ROOT
        Show-RepoStatus "Standalone Python Scanner"                              "Yellow" $STANDALONE
        Write-Host "`n  Shared-concern files (may need both repos updated):" -ForegroundColor Magenta
        Write-Host "    standalone/controls.py  — parser logic; commit to Standalone" -ForegroundColor DarkGray
        Write-Host "    references/*.md         — tracked in Scanner; read at runtime by Standalone" -ForegroundColor DarkGray
    }

    "push" {
        if (-not $m) {
            Write-Host "Error: commit message required.  Usage: .\manage.ps1 push -Repo both -m `"your message`"" -ForegroundColor Red
            exit 1
        }
        if (-not $Repo) {
            Write-Host "Error: -Repo required.  Options: scanner | standalone | both" -ForegroundColor Red
            exit 1
        }
        switch ($Repo) {
            "scanner"    { Invoke-Push "Multi-Modal-Scanner" "Cyan"   $ROOT       $m }
            "standalone" { Invoke-Push "Standalone"          "Yellow" $STANDALONE $m }
            "both"       {
                Invoke-Push "Multi-Modal-Scanner" "Cyan"   $ROOT       $m
                Invoke-Push "Standalone"          "Yellow" $STANDALONE $m
            }
        }
    }
}
