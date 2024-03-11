#include <iostream>

using namespace std;
void testing(int iAmInt, int iAmInt_2, std::string hello ) {
std::cout << "Hello From testing SUBROUTINE" << std::endl;
std::cout << iAmInt + iAmInt_2 << std::endl;
std::cout << hello << std::endl;
}
void helloWorld() {
std::cout << "Hello World" << std::endl;
}
string onePointThreeTwo() {
std::cout << "Hello World" << std::endl;
return "a";
}
float onePointThreeTwo_2(std::string hi ) {
std::cout << hi << std::endl;
return 1.33;
}
int main() {
std::cout << "Hello From Main SUBROUTINE" << std::endl;
testing(213, 1732672872,"umm");
helloWorld();
float helloWorldVar =  3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679;
std::cout <<  helloWorldVar << std::endl;
float onePointThreeTwo_var = onePointThreeTwo_2("wagwan");
std::cout << onePointThreeTwo_var << std::endl;
}
