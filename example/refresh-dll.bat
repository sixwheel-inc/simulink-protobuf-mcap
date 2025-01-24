@echo off
setlocal enabledelayedexpansion

echo "use cmake to build a windows and simulink friendly DLL"

call gather-sources.bat || exit 1 /b
call cmake-configure.bat || exit 1 /b
call cmake-build.bat || exit 1 /b

popd

