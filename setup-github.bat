@echo off
REM GitHub Setup Script for SafeEye
REM This script helps you push your SafeEye project to GitHub

echo ========================================
echo SafeEye GitHub Setup Script
echo ========================================
echo.

REM Check if git is initialized
if not exist ".git" (
    echo Initializing git repository...
    git init
    echo.
)

REM Check if .gitignore exists
if not exist ".gitignore" (
    echo WARNING: .gitignore not found!
    echo Please ensure .gitignore exists before proceeding.
    pause
    exit /b 1
)

echo Current git status:
git status --short
echo.

set /p GITHUB_USERNAME="Enter your GitHub username: "
set /p REPO_NAME="Enter repository name (default: safeye): "
if "%REPO_NAME%"=="" set REPO_NAME=safeye

echo.
echo Step 1: Adding all files...
git add .

echo.
set /p COMMIT_MSG="Enter commit message (default: Initial commit): "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Initial commit: SafeEye AI Theft Detection Platform

echo.
echo Step 2: Creating commit...
git commit -m "%COMMIT_MSG%"

echo.
echo Step 3: Checking for existing remote...
git remote -v | findstr origin >nul
if %errorlevel% equ 0 (
    echo Remote 'origin' already exists.
    set /p OVERWRITE="Do you want to overwrite it? (y/n): "
    if /i "%OVERWRITE%"=="y" (
        git remote remove origin
    ) else (
        echo Keeping existing remote. Please update manually if needed.
        goto :skip_remote
    )
)

echo Adding remote origin...
git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git

:skip_remote
echo.
echo Step 4: Setting branch to 'main'...
git branch -M main

echo.
echo Step 5: Pushing to GitHub...
echo.
echo IMPORTANT: Make sure you have created the repository on GitHub first!
echo Repository URL: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo.
set /p CONFIRM="Have you created the repository on GitHub? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo.
    echo Please create the repository first:
    echo 1. Go to https://github.com/new
    echo 2. Repository name: %REPO_NAME%
    echo 3. Description: AI-powered theft detection platform
    echo 4. DO NOT initialize with README
    echo 5. Click Create repository
    echo.
    pause
    exit /b 1
)

echo.
echo Pushing to GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! Your code has been pushed to GitHub!
    echo ========================================
    echo.
    echo Repository URL: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
    echo.
    echo Next steps:
    echo 1. Update README.md badges with your username
    echo 2. Add repository topics on GitHub
    echo 3. Enable Issues and Discussions
    echo 4. Create your first release
    echo.
) else (
    echo.
    echo ERROR: Push failed!
    echo.
    echo Troubleshooting:
    echo 1. Make sure the repository exists on GitHub
    echo 2. Check your GitHub credentials
    echo 3. Try: git pull origin main --allow-unrelated-histories
    echo.
)

pause

