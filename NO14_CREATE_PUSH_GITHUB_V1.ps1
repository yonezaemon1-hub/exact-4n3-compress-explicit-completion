param(
    [string]$RepoName = "exact-4n3-compress-explicit-completion",
    [string]$Owner = "yonezaemon1-hub"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoFull = "$Owner/$RepoName"

Write-Host "=== NO14 CREATE/PUSH GITHUB REPO V1 ==="
Write-Host "ROOT=$Root"
Write-Host "REPO=$RepoFull"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "STOP_GH_CLI_NOT_FOUND: install/authenticate GitHub CLI or create the empty public repo manually."
}

gh auth status
if ($LASTEXITCODE -ne 0) { throw "STOP_GH_NOT_AUTHENTICATED" }

$Exists = $false
gh repo view $RepoFull --json name 1>$null 2>$null
if ($LASTEXITCODE -eq 0) { $Exists = $true }

if (-not $Exists) {
    Write-Host "[1/4] Creating PUBLIC repository..."
    gh repo create $RepoFull --public --description "Proof and reproducibility package for an explicit total completion of a 3k+6-state binary synchronizing family with q0 compress-with-another threshold exactly 4n/3." --disable-issues --disable-wiki
    if ($LASTEXITCODE -ne 0) { throw "STOP_GH_REPO_CREATE_FAILED" }
} else {
    Write-Host "[1/4] Repository already exists; reusing."
}

Write-Host "[2/4] Initializing local git..."
Push-Location $Root
try {
    if (-not (Test-Path ".git")) {
        git init
        git branch -M main
    }
    git add .
    git status --short
    git commit -m "Prepare No.14 pre-DOI publication package"
    if ($LASTEXITCODE -ne 0) {
        git diff --cached --quiet
        if ($LASTEXITCODE -ne 0) { throw "STOP_GIT_COMMIT_FAILED" }
    }

    $Remote = git remote get-url origin 2>$null
    if ($LASTEXITCODE -ne 0) {
        git remote add origin "https://github.com/$RepoFull.git"
    }

    Write-Host "[3/4] Pushing main..."
    git push -u origin main
    if ($LASTEXITCODE -ne 0) { throw "STOP_GIT_PUSH_FAILED" }

    Write-Host "[4/4] Verifying public repository..."
    gh repo view $RepoFull --json name,url,visibility,defaultBranchRef
    if ($LASTEXITCODE -ne 0) { throw "STOP_GH_VERIFY_FAILED" }

    Write-Host "PASS_NO14_GITHUB_PRE_DOI=true"
}
finally {
    Pop-Location
}
