from compiler import Compiler_PC_CPP, FileImp
import argparse, os, sys, json
from Print import ErrorPrint, InfoPrint, WarnPrint
usage_c = "(Compiling ) "
usage_g = "(Generation) "
rootDir = os.getcwd()

parser = argparse.ArgumentParser("HEHE")
parser.add_argument("-g", "--gen", help=f"{usage_g}Generates a base project in the current working directory", type=bool, required=False, default=False, action=argparse.BooleanOptionalAction)
parser.add_argument("-f", "--file", help=f"{usage_c}The Input file", type=str, required=False)
parser.add_argument("-d", "--output_dir", help=f"{usage_c}dir of output files", type=str, required=False, default="output")
parser.add_argument("-n", "--project_name", help=f"{usage_c}name of the project", type=str, required=False)
parser.add_argument("-r", "--run", help=f"{usage_c}run the exe straight away after its been built", type=bool, required=False, default=False, action=argparse.BooleanOptionalAction)
includeFiles = ["builtins.h"]

args = parser.parse_args()
if args.gen == True and args.file is not None:
    ErrorPrint("cant use gen and file if you want to generate a project please use the -g True command")

if args.gen == False and args.file is not None:
    #TODO send file through a parser that will find imports and then will find them and convert them to C++ code thats added to the main file but is namespaced with the name of then other files (these are added 1st)
    
    Compiler_PC_CPP(args.file, args.output_dir, args.project_name, testing=True).Compile()
    #os.chdir(rootDir + "\\" + args.output_dir.replace("/", "\\"))
if args.gen == True:
    if args.project_name == None or args.project_name == "":
        ErrorPrint("Please use the -n flag with a name to specify a project name")
    else:
        ps = 'SUBROUTINE:int main THEN\nOUTPUT "Hello World"\nEND main'
        if os.path.exists(f"{os.getcwd()}\\{args.project_name}") == False:
            os.mkdir(f"{os.getcwd()}\\{args.project_name}")
        with open(f"{os.getcwd()}\\{args.project_name}\\{args.project_name}.pseudo" , "w")as f:
            f.write(ps)
        f.close()
        if " " in args.project_name:
            InfoPrint(f"Project Generated, Can Now use in the generated folder ' pcc -f '{args.project_name}' -d output ' to build the project")
        else:
            InfoPrint(f"Project Generated, Can Now use in the generated folder ' pcc -f {args.project_name} -d output ' to build the project")
    
if args.file is None and args.gen == False:
    ErrorPrint("Please Enter An input file using -f [FilePath] or use -h for the help prompt")