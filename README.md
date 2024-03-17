# PCC
Windows only at the moment
## Dependencies
    g++ already installed
    python

## How To Use
    - Download the installer from releases
    - Run The installer In A Command Line
    - Enter The Install Directory ie "D:/Apps/PCC"
        this will install PCC and G++
    - add the directory you installed to into the systems path 
    - Create a pseudocode file (check next section)
    - from the Terminal run the pcc -f [name of pseudocode file ] -d [output directory] -n [name for the compiled exe]


## TODO

    - In The myStd.h add GL Bindings so you can create opengl Apps and windows with   the language 
    - For Loop and While Loop Support
    - Add a Maths Lib with other builtins
    - 
## Generate a pseudo code project
    To create a pseudocode project you can use 
    pcc.exe -g True
    and answer the questions
        "What Do You Want To Name Your Project: " - name for the project, this is also where all files for the project will be stored
        "Where do you want your project to be stored: " - directory that will have the project directory 
        "Project to build output: " - the name for the build directory relative to project dir

## PseudoCode base file

    SUBROUTINE:int main THEN
    OUTPUT "HELLO WORLD"
    END main

## How To use the language

### User Input
    [varname]:[type] <-- USERINPUT

#### Example
    SUBROUTINE:int main THEN
    name:string <-- USERINPUT
    OUTPUT "HELLO " + name
    END main
-------
### Functions
Function Creation\
No Params

    SUBROUTINE:[type] [name] THEN 
    <---- CODE GOES HERE ---->
    END [name]
Params

    SUBROUTINE:[type](name:type,name:type,... ) [name] THEN 
    <---- CODE GOES HERE ---->
    END [name]
Function Invocation\
Without Parameters

    INVOKE [functionName]  

With parameters

    INVOKE [functionName](var1, var2, var3, ...)  

#### Example

    SUBROUTINE:void(name:string) hi THEN 
    OUTPUT "Hello " +  name
    END hi
    SUBROUTINE:int main THEN
    name_:string <-- USERINPUT
    hi(name_)
    END main

