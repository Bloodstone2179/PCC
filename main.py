from compiler import Compiler
import argparse, subprocess, os, shutil
usage_c = "(Compiling ) "
usage_g = "(Generation) "
rootDir = os.getcwd()
parser = argparse.ArgumentParser("HEHE")
parser.add_argument("-g", "--gen", help=f"{usage_g}Generates a base project in the current working directory", type=bool, required=False, default=False)
parser.add_argument("-f", "--file", help=f"{usage_c}The Input file", type=str, required=False)
parser.add_argument("-d", "--output_dir", help=f"{usage_c}dir of output files", type=str, required=False, default="./output/")
parser.add_argument("-n", "--project_name", help=f"{usage_c}name of the project", type=str, required=False, default="Application")
parser.add_argument("-r", "--run", help=f"{usage_c}run the exe straight away after its been built", type=bool, required=False, default=False)
args = parser.parse_args()
if args.gen == True and args.file is not None:
    print("cant use gen and file if you want to generate a project please use the ")
if args.gen == False:
    Compiler(args.file, args.output_dir, args.project_name).Compile()
    os.chdir(rootDir + "\\" + args.output_dir.replace("/", "\\"))
if args.gen == True:
    ps = 'SUBROUTINE:int main THEN\nOUTPUT "Hello World"\nEND main'
    #gen build file
    projName = input("What Do You Want To Name Your Project: ")
    output = input("Where do you want your project to be stored: ")
    output_proj = input("Where do you want your project to build files (relative to previous statement): ")
    buildFile_bat = f'@echo off\nset Output="{output}"\nset Input="{projName}.pseudo"\nset projName="{projName}"\npcc.exe -f %Input% -d {output_proj} -n %projName%'
    print(output + "\\" + projName)
    if os.path.isdir(output) == False:
        os.mkdir(os.getcwd() + "\\"+ output.replace("/", "\\"))
    os.chdir(output)
    if os.path.isdir(projName) == False:
        os.mkdir(projName)
    with open(f"{projName}\\build.bat", "w") as f:
        f.writelines(buildFile_bat)
    f.close()
    #generate the pseudo file
    with open(f"{projName}\\{projName}.pseudo", "w")as f:
        f.write(ps)
    f.close()
if args.run == True:
    print(f"running {args.project_name}")
    subprocess.run(f".\{args.project_name}.exe", shell=True)
    os.chdir(rootDir)