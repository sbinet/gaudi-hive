#include <list>
#include <string>
#include <map>
#include <set>
#include <vector>

namespace {

  struct _STLAddRflx_List_Instances {
    std::list<std::string>                           l_1;
    std::list<float>                                 l_2;
    std::list<double>                                l_3;
    std::list<signed int>                            l_4;
    std::list<signed long int>                       l_5;
  };

  struct _STLAddRflx_Map_Instances {
     std::map<int,int>                               m_1;
  };

  struct _STLAddRflx_Set_Instances {
    std::set<std::string>                            s_1;
    std::set<float>                                  s_2;
    std::set<double>                                 s_3;
    std::set<signed int>                             s_4;
    std::set<signed long int>                        s_5;
  };

  struct _STLAddRflx_Vector_Instances {
    std::vector<bool>                                v_1;
    std::vector<unsigned char>                       v_2;
    std::vector<signed char>                         v_3;
    std::vector<char>                                v_4;
    std::vector<std::string>                         v_5;
    std::vector<float>                               v_6;
    std::vector<double>                              v_7;
    std::vector<unsigned short int>                  v_8;
    std::vector<signed short int>                    v_9;
//icc already includes std::vector<unsigned> when instantiating std::vector<bool>
#ifndef __ICC
    std::vector<unsigned int>                        v_10;
#endif
    std::vector<signed int>                          v_11;
    std::vector<unsigned long int>                   v_12;
    std::vector<signed long int>                     v_13;
  };

  struct _STLAddRflx_String_Instance {
     std::string                                     s_1;
  };

}
