@echo off
set mypath=%cd%
set /p "version=Enter Version Name: "

pyinstaller --noconfirm --onefile --console --distpath "Releases/Win64/"%version% --name "pcc" --clean --add-data "SRC/compiler.py;."  "SRC/main.py" 
copy "./SRC/builtins.h" "./Releases/Win64/"%version%


pause