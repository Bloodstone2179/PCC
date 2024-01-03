from compiler import Compiler
import argparse, subprocess

parser = argparse.ArgumentParser("HEHE")
parser.add_argument("-f", "--file", help="The Input file", type=str, required=True)
parser.add_argument("-d", "--output_dir", help="dir of output files", type=str, required=False, default="./output/")
parser.add_argument("-n", "--project_name", help="name of the project", type=str, required=True, default="Application")
args = parser.parse_args()

Compiler(args.file, args.output_dir, args.project_name).Compile()
