@echo off

set /p "Output=Enter Output Directory: "
set /p "Input=Enter Input File: "
set /p "projName=Enter Project Name: "
set ext=exe
python .\main.py -f %Input% -d %Output% -n %projName%
echo %Output%/%projName%/%projName%.%ext%

del %Output%/%projName%/*.cpp
del %Output%/%projName%/*.h