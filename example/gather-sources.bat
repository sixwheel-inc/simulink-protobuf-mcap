@echo off
setlocal enabledelayedexpansion

echo "... Get 7z executable."
set "SEVEN_ZIP_PATH=C:\Program Files\7-Zip\7z.exe"
if not exist "%SEVEN_ZIP_PATH%" (
    echo 7-Zip not found at "%SEVEN_ZIP_PATH%"
	exit /b 1
)

git clean -fdx .

echo "... use bazel to retrieve and package third-party sources"
bazel build //third-party/mcap:cpp-source || exit /b 1

echo "... copy external source zips to here"
copy ..\bazel-bin\third-party\mcap\cpp-source.zip mcap.zip || exit /b 1

echo "... Unzip mcap cpp source into place"
mkdir mcap
"%SEVEN_ZIP_PATH%" x "mcap.zip" -o"mcap"
if %errorlevel% neq 0 (
    echo Error while unzipping mcap.zip
	exit /b 1
)

mkdir -p proto
echo "... Copy example.proto into place"
copy ..\example.proto proto

mkdir include
mkdir src

echo "... Copy sources into cmake dirs"
copy ..\example-busses.h .
copy ..\proto-to-busses.h .
copy ..\proto-to-busses.cpp .
copy ..\busses-to-proto.h .
copy ..\busses-to-proto.cpp .
copy ..\example-replay.h .
copy ..\example-replay.cpp .
copy ..\example-writer.h .
copy ..\example-writer.cpp .

echo "... Done gathering sources"
