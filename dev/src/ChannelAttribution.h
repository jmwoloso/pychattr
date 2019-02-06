#ifndef header
#define header 

using namespace std;
using namespace Rcpp;

string to_string(T pNumber);

RcppExport SEXP heuristic_models_cpp(SEXP Data_p, SEXP var_path_p, SEXP var_conv_p, SEXP var_value_p, SEXP sep_p);
RcppExport SEXP markov_model_cpp(SEXP Data_p, SEXP var_path_p, SEXP var_conv_p, SEXP var_value_p, SEXP var_null_p, SEXP order_p, SEXP nsim_p, SEXP max_step_p, SEXP out_more_p, SEXP sep_p);

#endif