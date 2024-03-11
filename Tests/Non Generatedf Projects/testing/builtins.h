#include <iostream>
#include <vector>
namespace builtinsNS {
    class builtinCL {
        public:
            std::vector<std::string> testFunction_stdVecOfStrings(){
                std::cout << "hello" << std::endl;
                std::vector<std::string> hi = {"Hello", "world"};
                return hi;
            }
            int GetStringLen(std::string input){
                int len = input.length();
                return len;
            }
            void AppendArray(std::vector<std::string> &arr, std::string Data){
                arr.push_back(Data);
            }
            void AppendArray(std::vector<int> &arr, int Data){
                arr.push_back(Data);
            }
            void AppendArray(std::vector<double> &arr, double Data){
                arr.push_back(Data);
            }
    };
}