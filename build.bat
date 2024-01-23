@echo off
set /p "Output=Enter Output Directory: "
set /p "Input=Enter Input File: "
set /p "projName=Enter Project Name: "
python .\main.py -f %Input% -d %Output% -n %projName%
.\%Output%%projName%.exe
cd  Tests