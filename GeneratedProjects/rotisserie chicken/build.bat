@echo off
set Output="GeneratedProjects"
set Input="rotisserie chicken.pseudo"
set projName="rotisserie chicken"
pcc.exe -f %Input% -d Builds -n %projName%