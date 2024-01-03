import os,subprocess,time

class Compiler:
    InputFile_PseudoCode_Lines = []
    includes = "#include <iostream>\n"
    C_Code = f"{includes}\nusing namespace std;\n"
    types = ["SUBROUTINE", "OUTPUT", "END", "INVOKE", "RETURN"]
    variable_types = ["string", "int","float"]
    vartypes_cpp = ["std::string", "int", "float"]
    functions = []
    
    
    def __init__(self, input_file: str = "program.psuedo", output_directory: str = "./output/", name: str = "Application"):
        self.input_file = input_file
        self.output_directory = output_directory
        self.name = name
    def readFile(self):
        with open(f"{os.getcwd()}/{self.input_file}", "r") as f:
            self.InputFile_PseudoCode_Lines = f.readlines()
        f.close()
        print(self.InputFile_PseudoCode_Lines)
    def StartMakingC_Code(self):
        for lineIn_inFile in self.InputFile_PseudoCode_Lines:
            '''
                - print what ever is at the end of the output
                - convert the subroutine to a function in c code
            '''
            first_split = lineIn_inFile.split(" ", maxsplit=1)
            if lineIn_inFile != "\n" and lineIn_inFile[0] != "#":
                if self.types[0] in first_split[0]  : # checking if subroutine
                    # get the subroutine and parse it separately
                    if "(" in first_split[0]: # checks for args
                        
                        SubRoutineType = lineIn_inFile.removeprefix("SUBROUTINE:").split("(")[0]
                        subName_base = lineIn_inFile.removeprefix("SUBROUTINE:").split(" ")
                        subName = subName_base[len(subName_base) - 2]
                        subArgs = lineIn_inFile.removeprefix("SUBROUTINE:" + SubRoutineType).removeprefix("(").replace(")", "").replace(subName + " THEN", "").split(",")
                        print(f"Return Type: {SubRoutineType}  Function Name {subName} ARGS: {subArgs}")
                        parameters = ""
                        for i in subArgs:
                            i = i.split()[0]
                            parsed = i.split(":")
                            type_= parsed[-1]
                            name_ = parsed[0]
                            print(f"Parsed: {parsed}")
                            '''
                                type : i.s [1]
                                name : i.s[0]
                            '''
                            if i in subArgs[-1]:
                                ending = " )"
                            else:
                                ending = ", "
                            
                            if type_ == "string":
                                parameters += "std::string " + name_ + ending
                            else:
                                parameters +=  type_ + " " + name_ + ending

                        
                        func = {"name" : subName,"type": SubRoutineType, "args" : parameters}
                        self.functions.append(func)
                        self.C_Code += SubRoutineType + " " + subName + "(" + parameters+ " {\n"
                    else: # if no args
                        SubRoutineType = lineIn_inFile.removeprefix("SUBROUTINE:").split(" ")[0]
                        subName_base = lineIn_inFile.removeprefix("SUBROUTINE:").split(" ")
                        subName = subName_base[len(subName_base) - 2]
                        self.C_Code += SubRoutineType + " " + subName + "() {\n"
                        func = {"name" : subName,"type": SubRoutineType, "args" : None}
                        self.functions.append(func)
                        print(f"Return Type: {SubRoutineType}  Function Name {subName} ARGS: NULL")
                elif self.types[1] in first_split[0] : # CHECKING IF OUTPUT
                    self.C_Code += f"std::cout << {first_split[1].removesuffix("\n")} << std::endl;\n"
                    
                if self.types[2] in first_split[0] : # checking for the end statement
                    self.C_Code += "}\n"
                if self.types[3] in first_split[0] : # checking if invoke (calls subroutine)
                    if "(" in first_split[1].removesuffix("\n"):
                        self.C_Code += f"{first_split[1].removesuffix("\n")};\n"
                    else:
                        self.C_Code += f"{first_split[1].removesuffix("\n")}();\n"
                if self.types[4] in first_split[0]:
                    self.C_Code += "return " +  first_split[-1].removesuffix("\n") +";\n"
                elif first_split[0].split(":")[0] not in self.types and "\n" not in first_split[0]: # assigning variables
                    varType = first_split[0].split(":")[-1]
                    varName = first_split[0].split(":")[0]
                    varContent = first_split[-1].removeprefix("<--").removesuffix("\n")
                    print(varContent)
                    if "INVOKE" in varContent.split(maxsplit=1)[0]:
                        if "(" in varContent.split(maxsplit=1)[1]:
                            varContent = f"{varContent.split(maxsplit=1)[1]}"
                        else:
                            varContent= f"{varContent.split(maxsplit=1)[1]}()"
                    typeIndex = self.variable_types.index(varType)
                    cpp_equiv = self.vartypes_cpp[typeIndex]
                    print(f"TYPE: {varType}  CPP EQUIV:{cpp_equiv} NAME : {varName} DATA: {varContent}")
                    self.C_Code += f"{cpp_equiv} {varName} = {varContent};\n"
    def writeToFile(self):
        if os.path.isdir(self.output_directory) == False:
            os.mkdir(self.output_directory)
        with open(self.output_directory + "\\" + self.name + ".cpp", "w") as f:
            f.writelines(self.C_Code)
        f.close()
    def Compile(self):
        s = time.time()
        self.readFile()
        self.StartMakingC_Code()
        self.writeToFile()
        print(f"TIME TO RUN {time.time() - s} seconds")
        subprocess.Popen(f"g++ {self.output_directory}\\{self.name}.cpp -o {self.output_directory}\\{self.name}.exe", shell=True)