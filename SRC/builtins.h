#include <iostream>
#include <vector>
#include <math.h>
namespace builtin {
    
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
    // TODO: 
    // - Create Math Library Extensions
    // 
    
    
}
namespace Maths {
    
    double Acos(double x)                 { return acos(x);            }
    double Asin(double x)                 { return asin(x);            }
    double Atan(double x)                 { return atan(x);            }
    double Atan2(double y, double x)      {return atan2(y,x);          }
    double Cos(double x)                  { return cos(x);             }
    double Cosh(double x)                 { return cosh(x);            }
    double Sin(double x)                  { return sin(x);             }
    double Sinh(double x)                 { return sinh(x);            }
    double Tan(double x)                  { return tan(x);             }
    double Tanh(double x)                 { return tanh(x);            }
    double Exp(double x)                  { return exp(x);             }
    double Frexp(double x, int *exponent) { return frexp(x,exponent);  }
    double Ldexp(double x, int exponent)  { return ldexp(x,exponent);  }
    double Log(double x)                  { return log(x);             }
    double Log10(double x)                { return log10(x);           }
    double Modf(double x, double *integer){ return modf(x,integer);    }
    double Pow(double x, double y)        { return pow(x,y);           }
    double Sqrt(double x)                 { return sqrt(x);            }
    double Ceil(double x)                 { return ceil(x);            }
    double Fabs(double x)                 { return fabs(x);            }
    double Floor(double x)                { return floor(x);           }
    double Fmod(double x, double y)       { return fmod(x,y);          }    
}