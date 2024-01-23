#include <iostream>
#include "D:\Docs\Code\Code-Projects\AQA PseudoCode transpiler/myStd.h"
using namespace std;
using namespace builtins;
builtins::builtin internalFunctions;

void pass() {
std::cout << "Enter Username: " << std::endl;
std::string a;
std::getline(std::cin, a);
if (a != "" ){
if (a == "james" ){
std::cout << "JAMES - Authenticated" << std::endl;
}
else if (a == "jane"){
std::cout << "JANE - Authenticated" << std::endl;
}
else {
std::cout << "USERNAME Not Accepted" << std::endl;
pass();
}
}
else {
std::cout << "Please Enter A Username" << std::endl;
pass();
}
}
int main() {
pass();
std::vector<std::string> testString = internalFunctions.hello();
std::cout << testString[0] + " " + testString[1] << std::endl;
testString.push_back("hello_2");
std::cout << testString[0] + " " + testString[1] + " " + testString[2] << std::endl;
}
