# PCC
Windows only at the moment
## Dependencies
    g++ already installed
    python

## How To Use
    - Download PCC.exe from releases
    - Install G++ 
    - Create a pseudocode file (check next section)
    - from the Terminal run the pcc -f [name of pseudocode file ] -d [output directory] -n [name for the compiled exe]

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

