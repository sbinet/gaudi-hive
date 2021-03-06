#include "ParsersStandardMiscCommon.h"

StatusCode Gaudi::Parsers::parse(std::map<unsigned int, std::string>& result, const std::string& input) {
    return Gaudi::Parsers::parse_(result, input);
}

StatusCode Gaudi::Parsers::parse(std::string& name, std::string& value ,
    const std::string& input ) {
  Skipper skipper;
  KeyValueGrammar<IteratorT, Skipper> g;
  KeyValueGrammar<IteratorT, Skipper>::ResultT result;
  std::string::const_iterator iter = input.begin();
  bool parse_result = qi::phrase_parse(iter, input.end(), g, skipper,
      result) && (iter==input.end());
  if (parse_result) {
    name = result.first;
    value = result.second;
  }
  return parse_result;
}

StatusCode Gaudi::Parsers::parse(std::map<std::string, std::pair<double, double> >& result, const std::string& input) {
    return Gaudi::Parsers::parse_(result, input);
}
