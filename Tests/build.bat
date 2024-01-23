@echo off
set Output="Tests"
set Input="ummmmm.pseudo"
set projName="ummmmm"
pcc.exe -f %Input% -d TestsBuilds -n %projName%