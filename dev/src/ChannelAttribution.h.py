#ifndef header
#define header 

using namespace std
using namespace Rcpp

def to_string(self, pNumber):

RcppExport SEXP heuristic_models_cpp(SEXP Data_p, var_path_p, var_conv_p, var_value_p, sep_p)
RcppExport SEXP markov_model_cpp(SEXP Data_p, var_path_p, var_conv_p, var_value_p, var_null_p, order_p, nsim_p, max_step_p, out_more_p, sep_p)

#endif