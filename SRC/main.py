from compiler import Compiler
import argparse, os, sys
usage_c = "(Compiling ) "
usage_g = "(Generation) "
rootDir = os.getcwd()

parser = argparse.ArgumentParser("HEHE")
parser.add_argument("-g", "--gen", help=f"{usage_g}Generates a base project in the current working directory", type=bool, required=False, default=False)
parser.add_argument("-f", "--file", help=f"{usage_c}The Input file", type=str, required=False)
parser.add_argument("-d", "--output_dir", help=f"{usage_c}dir of output files", type=str, required=False, default="./output/")
parser.add_argument("-n", "--project_name", help=f"{usage_c}name of the project", type=str, required=False, default="Application")
parser.add_argument("-r", "--run", help=f"{usage_c}run the exe straight away after its been built", type=bool, required=False, default=False, action=argparse.BooleanOptionalAction)
parser.add_argument("-v", "--version", help=f"Version Of PCC",required=False, type=bool,action=argparse.BooleanOptionalAction)
includeFiles = ["builtins.h"]
version_ = "v1.0.0.9-dev"
args = parser.parse_args()
if args.version is not None:
    print(f"Current Version: {version_}")
if args.gen == True and args.file is not None:
    print("cant use gen and file if you want to generate a project please use the -g True command")

if args.gen == False and args.file is not None:
    Compiler(args.file, args.output_dir, args.project_name, testing=True).Compile()
    #os.chdir(rootDir + "\\" + args.output_dir.replace("/", "\\"))
if args.gen == True and args.file == None :
    ps = 'SUBROUTINE:int main THEN\nOUTPUT "Hello World"\nEND main'

    with open(f"{os.getcwd()}\\program.pseudo" , "w")as f:
        f.write(ps)
    f.close()
    
if args.file is None :
    print("Please Enter An input file using -f [FilePath] or use -h for the help prompt")