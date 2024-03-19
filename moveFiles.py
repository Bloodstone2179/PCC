import shutil, json
from os import getcwd
installLocation = input("Enter PCC Install Location: ")
y = json.loads(open("VersionFile.json").read())["LatestReleaseVersion"]
pccDevLocation = getcwd() + "/Releases/Win64/" + y 
pcc_installer = pccDevLocation + "/pcc.exe"

shutil.copyfile(pcc_installer, installLocation + "/pcc.exe")

print("Building Finished Can Now Use new pcc version normally")