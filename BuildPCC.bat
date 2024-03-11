@echo off
set mypath=%cd%
set /p "version=Enter Version Name: "

pyinstaller --noconfirm --onefile --console --distpath "Releases/Win64/"%version% --name "pcc" --clean --add-data "SRC/compiler.py;."  "SRC/main.py" 
del VersionFile.json
echo {"LatestReleaseVersion" : "%version%"} >> VersionFile.json
