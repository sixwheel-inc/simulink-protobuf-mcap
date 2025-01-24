@echo off
setlocal enabledelayedexpansion

echo "... Build DLLs."
cmake --build build
if !errorlevel! neq 0 (
    echo "Failed cmake build"
    exit /b 1
)

