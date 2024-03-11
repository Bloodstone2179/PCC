#include <iostream>
#include <vector>
namespace builtins {
    class builtin {
        public:
            std::vector<std::string> hello(){
                std::cout << "hello" << std::endl;
                std::vector<std::string> hi = {"Hello", "world"};
                return hi;
            }
            int GetStringLen(std::string input){
                int len = input.length();
                return len;
            }
    };
}