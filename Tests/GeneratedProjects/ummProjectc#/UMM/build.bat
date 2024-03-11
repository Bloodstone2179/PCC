@echo off
set Output="ummProjectc#"
set Input="UMM.pseudo"
set projName="UMM"
pcc.exe -f %Input% -d builds -n %projName%