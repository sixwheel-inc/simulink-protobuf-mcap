@echo off
setlocal enabledelayedexpansion

echo "... Clean previous build."
rmdir /s /q build
mkdir build
