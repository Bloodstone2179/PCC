import shutil, json
from os import getcwd
installLocation = input("Enter PCC Install Location: ")
y = json.loads(open("VersionFile.json").read())["LatestReleaseVersion"]
pccDevLocation = getcwd() + "/Releases/Win64/" + y 
pcc_installer = pccDevLocation + "/pcc.exe"
b = getcwd() + "/SRC/builtins.h"
shutil.copyfile(pcc_installer, installLocation + "/pcc.exe")
shutil.copyfile(b, installLocation + "/g++_install/mingw64/include/c++/13.2.0/builtins.h")
print("Building Finished Can Now Use new pcc version normally")