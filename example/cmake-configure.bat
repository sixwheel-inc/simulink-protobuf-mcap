@echo off
setlocal enabledelayedexpansion

echo "... Load MSVC dev env via vcvars64.bat."
call "%MSVC_ROOT%\Auxiliary\Build\vcvars64.bat"
if !errorlevel! neq 0 (
    echo "Failed to load the MSVC dev environment"
    exit /b 1
)

echo "... Configure vcpkg, cmake, and ninja."
cmake -B build -G "Ninja" -DCMAKE_CXX_COMPILER="%MSVC_CL_EXE%" -DCMAKE_C_COMPILER="%MSVC_CL_EXE%" -DCMAKE_TOOLCHAIN_FILE="%MSVC_ROOT%\vcpkg\scripts\buildsystems\vcpkg.cmake" -DCMAKE_MAKE_PROGRAM="%MSVC_ROOT%\..\Common7\IDE\CommonExtensions\Microsoft\cmake\Ninja\ninja.exe" %CD%
if !errorlevel! neq 0 (
    echo "Failed to configure cmake build tree"
    exit /b 1
)

