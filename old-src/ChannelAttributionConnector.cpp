//#include <cstlib>

#include "ChannelAttributionConnector.h"
//#include "ChannelAttribution.h"

#ifdef __cplusplus
extern "C" {
#endif

// define the C functions that call the C++ functions

class Fx
{

 unsigned long int S;
 unsigned long int S0;
 unsigned long int S1;
 unsigned long int lrS0;
 unsigned long int lrS;
 unsigned long int non_zeros,nrows,val0,lval0,i,j,k,s0,lrs0i;

 public:
  Fx(unsigned long int nrow0,unsigned long int ncol0): S(nrow0,ncol0), S0(nrow0,ncol0), S1(nrow0,ncol0), lrS0(nrow0,0), lrS(nrow0,0), non_zeros(0), nrows(nrow0) {}
  void add(unsigned long int, unsigned long int,unsigned long int);
  void cum();
  unsigned long int sim(unsigned long int, double);
//  List tran_matx(vector<string>);

};

void Fx::add(unsigned long int ichannel_old, unsigned long int ichannel, unsigned long int vxi)
{

  val0=S(ichannel_old,ichannel); //riempire f.p. transizione con vxi
  if(val0==0){
   lval0=lrS0[ichannel_old];
   S0(ichannel_old,lval0)=ichannel;
   lrS0[ichannel_old]=lval0+1;
   ++non_zeros;
  }
  S(ichannel_old,ichannel)=val0+vxi;

}

void Fx::cum()
{

 for(i=0;i<nrows;i++){
  lrs0i=lrS0[i];
  if(lrs0i>0){
   S1(i,0)=S(i,S0(i,0));
   for(j=1;j<lrs0i;j++){
    S1(i,j)=S1(i,j-1)+S(i,S0(i,j));
   }
   lrS[i]=S1(i,lrs0i-1);
  }
 }

}


unsigned long int Fx::sim(unsigned long int c, double uni)
{

 s0=floor(uni*lrS[c]+1);

 for(k=0; k<lrS0[c]; k++){
  if(S1(c,k)>=s0){return(S0(c,k));}
 }

 return 0;

}


//List Fx::tran_matx(vector<string> vchannels)
//{
//
// unsigned long int mij,sm3;
// vector<string> vM1(non_zeros);
// vector<string> vM2(non_zeros);
// vector<double> vM3(non_zeros);
// vector<double> vsm;
// vector<unsigned long int> vk;
//
// k=0;
// for(i=0;i<nrows;i++){
//  sm3=0;
//  for(j=0;j<lrS0[i];j++){
//   mij=S(i,S0(i,j));
//   if(mij>0){
//      vM1[k]=vchannels[i];
//	  vM2[k]=vchannels[S0(i,j)];
//	  vM3[k]=mij;
//      sm3=sm3+mij;
//      ++k;
//	}
//  }
//
//  vsm.push_back(sm3);
//  vk.push_back(k);
//
// }//end for
//
// unsigned long int w=0;
// for(k=0;k<non_zeros;k++){
//  if(k==vk[w]){++w;}
//  vM3[k]=vM3[k]/vsm[w];
// }
//
// List res=List::create(Named("channel_from")=vM1, Named("channel_to") = vM2, Named("transition_probability") = vM3);
//
// return(res);
//
//}

}
