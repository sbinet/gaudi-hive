#include <list>
#include <utility>
#include <string>
#include <set>
#include <map>
#include <vector>

#if defined (__linux) || defined(__APPLE__)

#include <ext/hash_map>
#include <ext/hash_set>
#define tr1 __gnu_cxx 

#elif defined (_WIN32)

#include <hash_map>
#include <hash_set>
#define tr1 stdext

#endif

namespace {

  struct _STLRflx_HashContainer_Instances {
    tr1::hash_map<int, int>                          v_1;
    tr1::hash_map<int, double>                       v_2;
    tr1::hash_set<int>                               v_3;
    tr1::hash_set<char>                              v_4;
    tr1::hash_multimap<int, int>                     v_5;
    tr1::hash_multimap<int, double>                  v_6;
    tr1::hash_multiset<int>                          v_7;
    tr1::hash_multiset<char>                         v_8;
  };


  struct  _STLRflx_List_Instances {
    std::list<bool>                                  l_1;
    std::list<unsigned char>                         l_2;
    std::list<signed char>                           l_3;
    std::list<char>                                  l_4;
    std::list<long double>                           l_5;
    std::list<unsigned short int>                    l_6;
    std::list<signed short int>                      l_7;
    std::list<unsigned int>                          l_8;
    std::list<unsigned long int>                     l_9;
  };

  struct _STLRflx_Pair_Instances {
    std::pair<long int,double>                       p_1;
    std::pair<int,double>                            p_2;
    std::pair<int,int>                               p_3;
    std::pair<double,double>                         p_4;
    std::pair<std::string,int>                       p_5;
    std::pair<std::string,std::string>               p_6;
    std::pair<int,unsigned int>                      p_7;
  };

  struct  _STLRflx_Set_Instances {
    std::set<bool>                                   s_1;
    std::set<unsigned char>                          s_2;
    std::set<signed char>                            s_3;
    std::set<char>                                   s_4;
    std::set<long double>                            s_5;
    std::set<unsigned short int>                     s_6;
    std::set<signed short int>                       s_7;
    std::set<unsigned int>                           s_8;
    std::set<unsigned long int>                      s_9;
  };

  struct  _STLRflx_String_Instances {
    std::string                                      st;
  };

  struct  _STLRflx_Vector_Instances {
    std::vector<long double>                         v_1;
  };

  struct _STLRflx_VectorPair_Instances {
    std::vector<std::pair<int,int> >                 vp_1;
    std::vector<std::pair<int,double> >              vp_2;
    std::vector<std::pair<long int,double> >         vp_3;
    std::vector<std::pair<double,double> >           vp_4;
    std::vector<std::pair<std::string,int> >         vp_5;
    std::vector<std::pair<std::string,std::string> > vp_6;
    std::vector<std::pair<double, double> >          vp_7;
    std::vector<std::pair<unsigned int, unsigned int> > vp_8;
    std::vector<std::pair<double, std::pair<double, double> > > vp_9;
    std::vector<std::pair<int, unsigned int> >       vp_10;
     
  };

}
