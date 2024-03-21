import os,subprocess,time, termcolor,shutil, sys
def getResourcePath():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return base_path 


class FileImp:
    imported = []
    def __init__(self) -> None:
        pass
    def GetImportsOfAFile(self,file):
        with open(file, "r") as f:
            #print(file)
            r = f.readlines()
            for a in r:
                splits = a.split(" ", 1)
                if splits[0] == "IMPORT":
                    fileStatement = splits[1].strip()
                    self.imported.append(fileStatement)#
            f.close()
        
        #TODO - Make sure that parsing a file now uses the same functions that the old 1 uses

class ParseFileAndCreateNameSpace:
    C_Code = ""
    types = ["SUBROUTINE", "OUTPUT", "END", "INVOKE", "RETURN", "USERINPUT", "IF","ELSE","FOR", "ENDIF", "WHILE", "ELSEIF", "IMPORT"]
    variable_types = ["string", "int","float","double", "[]"]
    builtinFunctions = ["GetStringLen", "testFunction_stdVecOfStrings"]
    vartypes_cpp = ["std::string", "int", "double", "char","std::vector"]
    functions = []
    variables = []
    types_of_variable_in_the_cpp = []
    currentFuncName = None
    def __init__(self, file: str) -> None:
        self.C_Code = "namespace " + file.replace(".pseudo", "") + " {\n"
        self.Read_file = file
        self.Read()
    def Read(self):
        with open(self.Read_file, "r") as f:
            self.internals = f.readlines()
        f.close()
        self.Parse()
    def Parse(self):
        for lineIn_inFile in self.internals:
            '''
                - print what ever is at the end of the output
                - convert the subroutine to a function in c code
            '''
            
            first_split = lineIn_inFile.split(" ", maxsplit=1)
            
            first_split[0] = first_split[0]
            for i in first_split[0]:
                if i.isalnum() is not True:
                    if i == " ":
                        first_split[0][first_split[0].index(i)] = ""
                
            first_split[-1] = first_split[-1].removesuffix("\n")

            if lineIn_inFile != "\n" and lineIn_inFile[0] != "#" and lineIn_inFile[0] != "IMPORT":
                if self.types[0] in first_split[0]  : # checking if subroutine
                    # get the subroutine and parse it separately
                    if "(" in first_split[0]: # checks for args
                        
                        SubRoutineType = lineIn_inFile.removeprefix("SUBROUTINE:").split("(")[0]
                        subName_base = lineIn_inFile.removeprefix("SUBROUTINE:").split(" ")
                        subName = subName_base[len(subName_base) - 2]
                        self.currentFuncName = subName
                        subArgs = lineIn_inFile.removeprefix("SUBROUTINE:" + SubRoutineType).removeprefix("(").replace(")", "").replace(subName + " THEN", "").split(",")
                        parameters = ""
                        for i in subArgs:
                            i = i.split()[0]
                            parsed = i.split(":")
                            type_= parsed[-1]
                            name_ = parsed[0]
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
                        self.currentFuncName = subName
                        self.C_Code += SubRoutineType + " " + subName + "() {\n"
                        func = {"name" : subName,"type": SubRoutineType, "args" : None}
                        self.functions.append(func)
                elif self.types[1] in first_split[0] : # CHECKING TO SEE IF WE SHOULD OUTPUT
                    self.C_Code += f"std::cout << {first_split[1].removesuffix('\n')} << std::endl;\n"                  
                elif self.types[2] == first_split[0]: # checking for the end statement
                    self.C_Code += "}\n"
                elif self.types[9] in first_split[0]: # endif
                    self.C_Code += "}\n"    
                elif self.types[3] in first_split[0] : # checking if invoke (calls subroutine)
                    if "(" in first_split[1].removesuffix("\n"):
                        if first_split[1].split("(")[0] in self.builtinFunctions:
                            self.C_Code += f"{first_split[1].removesuffix("\n")};\n"
                        else:
                            self.C_Code += f"{first_split[1].removesuffix("\n")};\n"
                    else:
                        self.C_Code += f"{first_split[1].removesuffix("\n")}();\n"
                elif self.types[4] in first_split[0]: # RETURN
                    self.C_Code += "return " +  first_split[-1] +";\n"
                elif self.types[6] == first_split[0]: # IF
                    aa = first_split[-1].replace("THEN", "").removesuffix("\n")
                    self.C_Code += f'if ({aa.replace("AND", "&&").replace("OR", "||")})' + "{\n"
                elif self.types[7] == first_split[0]: # else
                    aa = first_split[-1].removesuffix("\n")
                    if aa == "ELSE":
                        cont = ""
                        else_type = "else"
                    
                    else:
                        cont = f"({aa.replace("AND", "&&").replace("OR", "||")})"
                        else_type = "else"
                    self.C_Code += "}\n" + f'{else_type} {cont}' + "{\n"
                elif self.types[11] == first_split[0]: # ElseIf
                    aa = first_split[-1].removesuffix("\n")
                    cont = f"({aa.replace("AND", "&&").replace("OR", "||")})"
                    self.C_Code += "}\n" + f'else if {cont}' + "{\n"
                elif self.types[12] == first_split[0]:
                    pass
                elif first_split[0].split(":")[0] not in self.types and "\n" not in first_split[0] and "." not in first_split[0] and " " not in first_split[0]: # assigning variables
                    varType = first_split[0].split(":")[-1]
                    varName = first_split[0].split(":")[0]
                    varContent = first_split[-1].removeprefix("<--").removesuffix("\n")
                    typeIndex = self.variable_types.index(varType.strip("[]"))
                    if varType == "float":
                        cpp_equiv = self.vartypes_cpp[2]
                    else:
                        cpp_equiv = self.vartypes_cpp[typeIndex]
                    if "INVOKE" in varContent.split(maxsplit=1)[0] and "[" not in varType:
                        if "(" in varContent.split(maxsplit=1)[1]:
                            if varContent.split(maxsplit=1)[1].split("(")[0] in self.builtinFunctions:
                                varContent = f"{varContent.split(maxsplit=1)[1]}"
                            else:
                                varContent = f"{varContent.split(maxsplit=1)[1]}"
                        else:
                            varContent= f"{varContent.split(maxsplit=1)[1]}()"
                        
                        self.C_Code += f"{cpp_equiv} {varName} = {varContent};\n"
                    elif "[" in varType:
                        if "[" in varContent.split(maxsplit=1)[0]:
                            self.C_Code += f"std::vector<{cpp_equiv}> {varName} = " + "{"+ f"{varContent.split(maxsplit=1)[0].replace("[","").replace("]","")}" +"}"+ ";\n"
                        elif "INVOKE" in varContent.split(maxsplit=1)[0]:
                            if varContent.split(maxsplit=1)[1].split("(")[0] in self.builtinFunctions:
                                self.C_Code += f"std::vector<{cpp_equiv}> {varName} = {varContent.split(maxsplit=1)[1]};\n"
                            else:
                                self.C_Code += f"std::vector<{cpp_equiv}> {varName} = {varContent.split(maxsplit=1)[1]};\n"
                        else:
                            self.C_Code += f"std::vector<{cpp_equiv}> {varName};\n"
                   
                    elif "USERINPUT" in varContent.split(maxsplit=1)[0]:
                        self.C_Code += f"{cpp_equiv} {varName};\nstd::getline(std::cin, {varName});\n"
                    else:
                        self.C_Code += f"{cpp_equiv} {varName} = {varContent};\n"
                    self.variables.append(varName)
                elif first_split[0].split(".")[0] in self.variables or first_split[0].split(" ")[0]:
                    self.C_Code += f"{first_split[0]};\n"
    def Get(self):
        return self.C_Code + "}\n"
class Compiler_PC_CPP:
    InputFile_PseudoCode_Lines = []
    includes = f'#include <iostream>\n#include "builtins.h"'
    C_Code = f"{includes}\nusing namespace std;\nusing namespace builtin;\n"
    #             0           1        2       3         4           5        6     7      8        9       10       11
    types = ["SUBROUTINE", "OUTPUT", "END", "INVOKE", "RETURN", "USERINPUT", "IF","ELSE","FOR", "ENDIF", "WHILE", "ELSEIF", "IMPORT"]
    variable_types = ["string", "int","float","double", "[]"]
    builtinFunctions = ["GetStringLen", "testFunction_stdVecOfStrings"]
    vartypes_cpp = ["std::string", "int", "double", "char","std::vector"]
    functions = []
    variables = []
    types_of_variable_in_the_cpp = []
    outType = "exe"
    currentFuncName = None
    def __init__(self, input_file: str = "program.psuedo", output_directory: str = "output", name: str = "Application", outType: str = "exe", testing: bool = False, imports=None):
        self.input_file = input_file
        self.output_directory = output_directory
        self.name = name
        self.outType = outType
        self.test = testing
        self.importedFiles = []
        
        self.FileImporter = FileImp
        self.FileImporter.GetImportsOfAFile(self.FileImporter,input_file)
        for i in self.FileImporter.imported:
            self.FileImporter.GetImportsOfAFile(self.FileImporter,i)
        self.importedFiles = self.FileImporter.imported
        for imports in self.FileImporter.imported:
            namespace = ParseFileAndCreateNameSpace(imports)
            code = namespace.Get()
            self.C_Code += code
    def readFile(self):
        with open(f"{os.getcwd()}/{self.input_file}", "r") as f:
            self.InputFile_PseudoCode_Lines = f.readlines()
        f.close()
        #print(self.InputFile_PseudoCode_Lines)
    def StartMakingC_Code(self):
        for lineIn_inFile in self.InputFile_PseudoCode_Lines:
            '''
                - print what ever is at the end of the output
                - convert the subroutine to a function in c code
            '''
            
            first_split = lineIn_inFile.split(" ", maxsplit=1)
            
            first_split[0] = first_split[0]
            for i in first_split[0]:
                if i.isalnum() is not True:
                    if i == " ":
                        print(first_split[0].index(i))
                        first_split[0][first_split[0].index(i)] = ""
                
            first_split[-1] = first_split[-1].removesuffix("\n")

            if lineIn_inFile != "\n" and lineIn_inFile[0] != "#" and lineIn_inFile[0] != "IMPORT":
                if self.types[0] in first_split[0]  : # checking if subroutine
                    # get the subroutine and parse it separately
                    if "(" in first_split[0]: # checks for args
                        
                        SubRoutineType = lineIn_inFile.removeprefix("SUBROUTINE:").split("(")[0]
                        subName_base = lineIn_inFile.removeprefix("SUBROUTINE:").split(" ")
                        subName = subName_base[len(subName_base) - 2]
                        self.currentFuncName = subName
                        subArgs = lineIn_inFile.removeprefix("SUBROUTINE:" + SubRoutineType).removeprefix("(").replace(")", "").replace(subName + " THEN", "").split(",")
                        parameters = ""
                        for i in subArgs:
                            i = i.split()[0]
                            parsed = i.split(":")
                            type_= parsed[-1]
                            name_ = parsed[0]
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
                        self.currentFuncName = subName
                        self.C_Code += SubRoutineType + " " + subName + "() {\n"
                        func = {"name" : subName,"type": SubRoutineType, "args" : None}
                        self.functions.append(func)
                elif self.types[1] in first_split[0] : # CHECKING TO SEE IF WE SHOULD OUTPUT
                    self.C_Code += f"std::cout << {first_split[1].removesuffix('\n')} << std::endl;\n"                  
                elif self.types[2] == first_split[0]: # checking for the end statement
                    self.C_Code += "}\n"
                elif self.types[9] in first_split[0]: # endif
                    self.C_Code += "}\n"    
                elif self.types[3] in first_split[0] : # checking if invoke (calls subroutine)
                    if "(" in first_split[1].removesuffix("\n"):
                        if first_split[1].split("(")[0] in self.builtinFunctions:
                            self.C_Code += f"{first_split[1].removesuffix("\n")};\n"
                        else:
                            self.C_Code += f"{first_split[1].removesuffix("\n")};\n"
                    else:
                        self.C_Code += f"{first_split[1].removesuffix("\n")}();\n"
                elif self.types[4] in first_split[0]: # RETURN
                    self.C_Code += "return " +  first_split[-1] +";\n"
                elif self.types[6] == first_split[0]: # IF
                    aa = first_split[-1].replace("THEN", "").removesuffix("\n")
                    self.C_Code += f'if ({aa.replace("AND", "&&").replace("OR", "||")})' + "{\n"
                elif self.types[7] == first_split[0]: # else
                    aa = first_split[-1].removesuffix("\n")
                    if aa == "ELSE":
                        cont = ""
                        else_type = "else"
                    
                    else:
                        cont = f"({aa.replace("AND", "&&").replace("OR", "||")})"
                        else_type = "else"
                    self.C_Code += "}\n" + f'{else_type} {cont}' + "{\n"
                elif self.types[11] == first_split[0]: # ElseIf
                    aa = first_split[-1].removesuffix("\n")
                    cont = f"({aa.replace("AND", "&&").replace("OR", "||")})"
                    self.C_Code += "}\n" + f'else if {cont}' + "{\n"
                elif self.types[12] == first_split[0]: #IMPORT
                    pass
                elif first_split[0].split(":")[0] not in self.types and "\n" not in first_split[0] and "." not in first_split[0] and " " not in first_split[0]: # assigning variables
                    varType = first_split[0].split(":")[-1]
                    varName = first_split[0].split(":")[0]
                    varContent = first_split[-1].removeprefix("<--").removesuffix("\n")
                    typeIndex = self.variable_types.index(varType.strip("[]"))
                    if varType == "float":
                        cpp_equiv = self.vartypes_cpp[2]
                    else:
                        cpp_equiv = self.vartypes_cpp[typeIndex]
                    if "INVOKE" in varContent.split(maxsplit=1)[0] and "[" not in varType:
                        if "(" in varContent.split(maxsplit=1)[1]:
                            if varContent.split(maxsplit=1)[1].split("(")[0] in self.builtinFunctions:
                                varContent = f"{varContent.split(maxsplit=1)[1]}"
                            else:
                                varContent = f"{varContent.split(maxsplit=1)[1]}"
                        else:
                            varContent= f"{varContent.split(maxsplit=1)[1]}()"
                        
                        self.C_Code += f"{cpp_equiv} {varName} = {varContent};\n"
                    elif "[" in varType:
                        print(varContent.split(maxsplit=1))
                        if "[" in varContent.split(maxsplit=1)[0]:
                            self.C_Code += f"std::vector<{cpp_equiv}> {varName} = " + "{"+ f"{varContent.split(maxsplit=1)[0].replace("[","").replace("]","")}" +"}"+ ";\n"
                        elif "INVOKE" in varContent.split(maxsplit=1)[0]:
                            if varContent.split(maxsplit=1)[1].split("(")[0] in self.builtinFunctions:
                                self.C_Code += f"std::vector<{cpp_equiv}> {varName} = {varContent.split(maxsplit=1)[1]};\n"
                            else:
                                self.C_Code += f"std::vector<{cpp_equiv}> {varName} = {varContent.split(maxsplit=1)[1]};\n"
                        else:
                            self.C_Code += f"std::vector<{cpp_equiv}> {varName};\n"
                   
                    elif "USERINPUT" in varContent.split(maxsplit=1)[0]:
                        self.C_Code += f"{cpp_equiv} {varName};\nstd::getline(std::cin, {varName});\n"
                    else:
                        self.C_Code += f"{cpp_equiv} {varName} = {varContent};\n"
                    self.variables.append(varName)
                    print(self.variables)
                elif first_split[0].split(".")[0] in self.variables or first_split[0].split(" ")[0]:
                    print(first_split)
                    self.C_Code += f"{first_split[0]};\n"
                    print(self.variables)
                    
                    
    def writeToFile(self):
        if os.path.isdir(self.output_directory) == False:
            os.mkdir(os.getcwd() + "\\"+ self.output_directory.replace("/", "\\"))
        with open(self.output_directory + "\\" + self.name + ".cpp", "w") as f:
            f.writelines(self.C_Code)
        f.close()
    def Compile(self):
        s = time.time()
        self.readFile()
        self.StartMakingC_Code()
        self.writeToFile()
        installLoc = getResourcePath()
        if self.test == True:
            installLoc = "D:/Apps/PCC"
        if ":" not in self.output_directory:
            self.output_directory = f"'{os.getcwd()}\\{self.output_directory}"
        print(self.output_directory + f"\\{self.name}.cpp")
        termcolor.cprint("<-------------------- BUILT EXE -------------------->","green")
        subprocess.run(f"{installLoc}\\g++_install\\mingw64\\bin\\g++ {self.output_directory}\\{self.name}.cpp' -o {self.output_directory}\\{self.name}.{self.outType}'", shell=True)
        termcolor.cprint("<-------------------- BUILT EXE -------------------->","blue")
        print(f"TIME TO RUN {time.time() - s} seconds")
        #os.remove(f"{self.output_directory}\\{self.name}.cpp")