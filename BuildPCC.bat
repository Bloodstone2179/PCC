@echo off
set mypath=%cd%
set /p "version=Enter Version Name: "

pyinstaller --noconfirm --console --onefile --distpath "Releases/Win64/"%version% --name "pcc" --add-data "SRC/BetterPrint.py;." --add-data "SRC/compiler.py;."  "SRC/main.py"
del VersionFile.json
echo {"LatestReleaseVersion" : "%version%"} >> VersionFile.json

python moveFiles.py