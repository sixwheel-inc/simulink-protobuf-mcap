@echo off
setlocal enabledelayedexpansion

echo "... Run unittests."
ctest --test-dir build --verbose
if !errorlevel! neq 0 (
    echo "Failed cmake test"
    exit /b 1
)

