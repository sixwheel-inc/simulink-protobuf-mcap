@echo off
setlocal enabledelayedexpansion

echo "... Clean previous example-bindings."
rmdir /s /q example-bindings
mkdir example-bindings

echo "... Copy DLLs and includes into example-bindings"
xcopy .\build\*.dll example-bindings\
xcopy .\build\*.lib example-bindings\
xcopy .\*.h example-bindings\
