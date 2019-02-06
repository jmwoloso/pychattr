#define __GXX_EXPERIMENTAL_CXX0X__ 1

#include <iostream>
#include <string>
#include <vector>
#include <random>
#include <numeric>
#include <list>

##include <RcppArmadillo.h>
#define ARMA_USE_CXX11
#define ARMA_64BIT_WORD

#ifndef BEGIN_RCPP
#define BEGIN_RCPP
#endif
 
#ifndef END_RCPP
#define END_RCPP
#endif

using namespace std
#using namespace Rcpp
using namespace arma

template <typename T>
def to_string(self, pNumber):
 ostringstream oOStrStream
 oOStrStream << pNumber
 return oOStrStream.str()



##########################################################################################/

#RcppExport SEXP heuristic_models_cpp(SEXP Data_p, var_path_p, var_conv_p, var_value_p, sep_p)
##
# BEGIN_RCPP
#
# #inp.a
#
# List Data(Data_p)
#
# CharacterVector var_path_0(var_path_p)
# var_path = Rcpp.as<string>(var_path_0)
#
# CharacterVector var_conv_0(var_conv_p)
# var_conv = Rcpp.as<string>(var_conv_0)
#
# CharacterVector var_value_0(var_value_p)
# var_value = Rcpp.as<string>(var_value_0)
#
# CharacterVector sep_0(sep_p)
# sep = Rcpp.as<string>(sep_0)
#
# #inp.b
#
# bool flg_var_value
# flg_var_value=0
# if var_value.compare("0")!=0:#  flg_var_value=1
#
#
# vy0 = Data[var_path]
# vector<string> vy = Rcpp.as<vector<string> >(vy0)
#
# vc0 = Data[var_conv]
# vector<long long int> vc = Rcpp.as<vector<long long int> >(vc0)
#
# vector<double> vv
# if flg_var_value==1:#  vv0 = Data[var_value]
#  vv = Rcpp.as<vector<double> >(vv0)
#
#
# long long int i,j,k,lvy,ssize
# bool cfirst
# unsigned long int start_pos,end_pos
# long long int nchannels
# string s,channel,channel_first,channel_last
#
# lvy=(long long int) vy.size()
# nchannels=0
#
# map<string, long int> mp_channels
# vector<string> vchannels
#
# map<string, mp_first_conv
# map<string, mp_first_val
# map<string, mp_last_conv
# map<string, mp_last_val
# map<string, mp_linear_conv
# map<string, mp_linear_val
# map<string, mp0_linear_conv
# map<string, mp0_linear_val
#
# vector<string> vchannels_unique
# double nchannels_unique
# string kchannel
# long long int n_path_length
#
# for(i=0;i<lvy;i++)#
#  s=vy[i]
#
#  s+=sep[0]
#  ssize=(long long int) s.size()
#  channel=""
#  j=0
#  nchannels_unique=0
#  vchannels_unique.clear()
#
#  n_path_length=0
#  mp0_linear_conv.clear()
#  mp0_linear_val.clear()
#
#  while(j<ssize)#
#   cfirst=1
#   while(s[j]!=sep[0])#	if cfirst==0:#     if s[j]!=' ':#	  end_pos=j
#
#    }elif (cfirst==1) & (s[j]!=' '):#	 cfirst=0
#	 start_pos=j
#	 end_pos=j
#
#    ++j
#
#
#   if cfirst==0:#    channel=s.substr(start_pos,(end_pos-start_pos+1))
#
#    if mp_channels.find(channel) == mp_channels.end():#	 mp_channels[channel]=nchannels
#	 vchannels.push_back(channel)
#	 ++nchannels
#
#     mp_first_conv[channel]=0
#	 mp_last_conv[channel]=0
#	 mp_linear_conv[channel]=0
#	 mp0_linear_conv[channel]=0
#
#	 if flg_var_value==1:#	  mp_first_val[channel]=0
#	  mp_last_val[channel]=0
#	  mp_linear_val[channel]=0
#	  mp0_linear_val[channel]=0
#
#
#
#
#    #lista canali unici
#    if nchannels_unique==0:#     vchannels_unique.push_back(channel)
#	 ++nchannels_unique
#    }elif find(vchannels_unique.begin(),vchannels_unique.end(),channel)==vchannels_unique.end():#	 vchannels_unique.push_back(channel)
#	 ++nchannels_unique
#
#
# 	mp0_linear_conv[channel]=mp0_linear_conv[channel]+vc[i]
#    if flg_var_value==1:#	 mp0_linear_val[channel]=mp0_linear_val[channel]+vv[i]
#
#	++n_path_length
#
#    channel_last=channel
#
#   }#end cfirst
#
#   channel=""
#   ++j
#
#  }#end while j
#
#  channel_first=vchannels_unique[0]
#  mp_first_conv[channel_first]=mp_first_conv[channel_first]+vc[i]
#
#  mp_last_conv[channel_last]=mp_last_conv[channel_last]+vc[i]
#
#  #linear
#  for(k=0;k<nchannels_unique;k++)#    kchannel=vchannels_unique[k]
#    mp_linear_conv[kchannel]=mp_linear_conv[kchannel]+(mp0_linear_conv[kchannel]/n_path_length)
#
#
#  if flg_var_value==1:#   mp_first_val[channel_first]=mp_first_val[channel_first]+vv[i]
#   mp_last_val[channel_last]=mp_last_val[channel_last]+vv[i]
#   for(k=0;k<nchannels_unique;k++)#    kchannel=vchannels_unique[k]
#    mp_linear_val[kchannel]=mp_linear_val[kchannel]+(mp0_linear_val[kchannel]/n_path_length)
#
#
#
#
# }#end for i
#
# vector<double> vfirst_conv(nchannels)
# vector<double> vlast_conv(nchannels)
# vector<double> vlinear_conv(nchannels)
#
# vector<double> vfirst_val(nchannels)
# vector<double> vlast_val(nchannels)
# vector<double> vlinear_val(nchannels)
#
# for(k=0;k<nchannels;k++)#  kchannel=vchannels[k]
#  vfirst_conv[k]=mp_first_conv[kchannel]
#  vlast_conv[k]=mp_last_conv[kchannel]
#  vlinear_conv[k]=mp_linear_conv[kchannel]
#
#  if flg_var_value==1:#   vfirst_val[k]=mp_first_val[kchannel]
#   vlast_val[k]=mp_last_val[kchannel]
#   vlinear_val[k]=mp_linear_val[kchannel]
#
#
#
#
# if flg_var_value==1:#  return List.create(Named("channel_name")=vchannels, Named("first_touch_conversions") = vfirst_conv, Named("first_touch_value") = vfirst_val, Named("last_touch_conversions") = vlast_conv, Named("last_touch_value") = vlast_val, Named("linear_touch_conversions") = vlinear_conv, Named("linear_touch_value") = vlinear_val)
# }else:
#  return List.create(Named("channel_name")=vchannels, Named("first_touch") = vfirst_conv, Named("last_touch") = vlast_conv, Named("linear_touch") = vlinear_conv)
#
#
# END_RCPP
#
#}#end heuristic_models_cpp


#########################################################################################/



#Classe funzione di ripartizione

class Fx
 
 SpMat<unsigned long int> S
 SpMat<unsigned long int> S0
 SpMat<unsigned long int> S1
 vector<unsigned long int> lrS0
 vector<unsigned long int> lrS; 
 unsigned long int non_zeros,nrows,val0,lval0,i,j,k,s0,lrs0i
 
 public:
  Fx(unsigned long int nrow0, long int ncol0): S(nrow0,ncol0), S0(nrow0,ncol0), S1(nrow0,ncol0), lrS0(nrow0,0), lrS(nrow0,0), non_zeros(0), nrows(nrow0) {
  void add(unsigned long int, long int, long int)
  void cum()
  unsigned long int sim(unsigned long int, double); 
  List tran_matx(vector<string>); 
	 
};  

def add(self, long int ichannel_old, long int ichannel, long int vxi):
  
  val0=S(ichannel_old,ichannel); #riempire f.p. transizione con vxi
  if val0==0:   lval0=lrS0[ichannel_old]
   S0(ichannel_old,lval0)=ichannel
   lrS0[ichannel_old]=lval0+1
   ++non_zeros

  S(ichannel_old,ichannel)=val0+vxi; 
  
} 

def cum(self):

 for(i=0;i<nrows;i++)  lrs0i=lrS0[i]
  if lrs0i>0:   S1(i,0)=S(i,S0(i,0))
   for(j=1;j<lrs0i;j++)    S1(i,j)=S1(i,j-1)+S(i,S0(i,j))

   lrS[i]=S1(i,lrs0i-1)
  }   
 }	
  



unsigned long int Fx.sim(unsigned long int c, uni) 
 
 s0=floor(uni*lrS[c]+1)
 
 for(k=0; k<lrS0[c]; k++){   
  if(S1(c,k)>=s0){return(S0(c,k));


 return 0
	



def tran_matx(self, vchannels):

 unsigned long int mij,sm3
 vector<string> vM1(non_zeros)
 vector<string> vM2(non_zeros)
 vector<double> vM3(non_zeros)
 vector<double> vsm
 vector<unsigned long int> vk
 
 k=0
 for(i=0;i<nrows;i++)  sm3=0
  for(j=0;j<lrS0[i];j++)   mij=S(i,S0(i,j))
   if(mij>0){   
      vM1[k]=vchannels[i]
	  vM2[k]=vchannels[S0(i,j)]
	  vM3[k]=mij
      sm3=sm3+mij
      ++k


  
  vsm.push_back(sm3)
  vk.push_back(k)
  
 }#end for
 
 unsigned long int w=0
 for(k=0;k<non_zeros;k++)  if(k==vk[w]){++w;
  vM3[k]=vM3[k]/vsm[w]; 

  
 List res=List.create(Named("channel_from")=vM1, Named("channel_to") = vM2, Named("transition_probability") = vM3); 

 return(res)
 



#RcppExport SEXP markov_model_cpp(SEXP Data_p, var_path_p, var_conv_p, var_value_p, var_null_p, order_p, nsim_p, max_step_p, out_more_p, sep_p)
##
# BEGIN_RCPP
#
# #inp.a
#
# List Data(Data_p)
#
# CharacterVector var_path_0(var_path_p)
# var_path = Rcpp.as<string>(var_path_0)
#
# CharacterVector var_conv_0(var_conv_p)
# var_conv = Rcpp.as<string>(var_conv_0)
#
# CharacterVector var_value_0(var_value_p)
# var_value = Rcpp.as<string>(var_value_0)
#
# CharacterVector var_null_0(var_null_p)
# var_null = Rcpp.as<string>(var_null_0)
#
# NumericVector order_0(order_p)
# unsigned long long order = Rcpp.as<unsigned long long int>(order_0)
#
# NumericVector nsim_0(nsim_p)
# unsigned long long nsim = Rcpp.as<unsigned long long int>(nsim_0)
#
# NumericVector max_step_0(max_step_p)
# unsigned long long max_step = Rcpp.as<unsigned long long int>(max_step_0)
#
# NumericVector out_more_0(out_more_p)
# unsigned long long out_more = Rcpp.as<unsigned long long int>(out_more_0)
#
# CharacterVector sep_0(sep_p)
# sep = Rcpp.as<string>(sep_0)
#
# #inp.b
#
# bool flg_var_value
# flg_var_value=0
# if var_value.compare("0")!=0:#  flg_var_value=1
#
#
# bool flg_var_null
# flg_var_null=0
# if var_null.compare("0")!=0:#  flg_var_null=1
#
#
# vy0 = Data[var_path]
# vector<string> vy = Rcpp.as<vector<string> >(vy0)
#
# vc0 = Data[var_conv]
# vector<unsigned long int> vc = Rcpp.as<vector<unsigned long int> >(vc0)
#
# vector<double> vv
# if flg_var_value==1:#  vv0 = Data[var_value]
#  vv = Rcpp.as<vector<double> >(vv0)
#
#
# vector<unsigned long int> vn
# if flg_var_null==1:#  vn0 = Data[var_null]
#  vn = Rcpp.as<vector<unsigned long int> >(vn0)
#
#
# unsigned long int i,j,k,lvy,ssize
# unsigned long int nchannels,nchannels_sim,npassi
# bool cfirst
# unsigned long int start_pos,end_pos
# string s,channel,path
# map<string, long int> mp_channels,mp_channels_sim
# map<unsigned long int, long int> mp_npassi
# vector<unsigned long int> vnpassi
#
# #cout << "Processed 1/4" << endl
#
# lvy=(unsigned long int) vy.size()
#
# ###########
# #CODIFICA DA ONE STEP
# ###########
#
# #mappa dei conversion value
# unsigned long int l_vui=0
# map<double, long int> mp_vui
# vector<double> v_vui
# double vui
#
# vector<string> rchannels
# unsigned long int lrchannels,j0,z
# string channel_j
#
# vector<long int> vchannels_sim_id(order)
# map<unsigned long int, int>> mp_channels_sim_id
#
# nchannels=0
# nchannels_sim=0
#
# vector<string> vy2(lvy)
#
# mp_channels["(start)"]=0
# vector<string> vchannels
# vchannels.push_back("(start)")
# ++nchannels
#
# vector<string> vchannels_sim
# for(z=0;z<order;z++)#  vchannels_sim_id[z]=-1
#
# if order>1:#  mp_channels_sim["(start)"]=nchannels_sim
#  vchannels_sim.push_back("(start)")
#  vchannels_sim_id[0]=nchannels_sim
#  mp_channels_sim_id[nchannels_sim]=vchannels_sim_id
#  ++nchannels_sim
#
#
#
# #definizione mappa conversion value
# if flg_var_value==1:#  for(i=0;i<lvy;i++)#   if vc[i]>0:#	vui=vv[i]/vc[i]
#    if mp_vui.find(vui)==mp_vui.end():#     mp_vui[vui]=l_vui
#     v_vui.push_back(vui)
#     ++l_vui
#
#
#
#
#
# for(i=0;i<lvy;i++)#
#  s=vy[i]
#  s+=sep[0]
#  ssize=(unsigned long int) s.size()
#  channel=""
#  path=""
#  j=0
#  npassi=0
#  rchannels.clear()
#
#  #medium.touch
#
#  while(j<ssize)#
#   cfirst=1
#   while(s[j]!=sep[0])#	if cfirst==0:#     if s[j]!=' ':#	  end_pos=j
#
#    }elif (cfirst==1) & (s[j]!=' '):#	 cfirst=0
#	 start_pos=j
#	 end_pos=j
#
#    ++j
#
#
#   if cfirst==0:#    channel=s.substr(start_pos,(end_pos-start_pos+1))
#
#    if mp_channels.find(channel) == mp_channels.end():#     mp_channels[channel]=nchannels
#     vchannels.push_back(channel)
#     ++nchannels
#
#
#    if order==1:#
#     if npassi==0:#      path="0 "
#     }else:
#      path+=" "
#
#
#     path+=to_string(mp_channels[channel])
#     ++npassi
#
#    }else:
#
#     rchannels.push_back(channel)
#
#
#
#   }#if end_pos
#
#   channel=""
#   ++j
#
#  }#end while channel
#
#  if order>1:#
#	lrchannels=rchannels.size()
#	for(z=0;z<order;z++)#	 vchannels_sim_id[z]=-1
#
#
#    if lrchannels>(order-1):#
#     npassi=lrchannels-order+1
#
#     for(k=0;k<npassi;k++)#
#	  channel=""
#	  channel_j=""
#
#  	  z=0
#	  j0=k+order
#	  for(j=k;j<j0;j++)#	    channel_j=rchannels[j]
#	    channel+=channel_j
#	    vchannels_sim_id[z]=mp_channels[channel_j]
#	    ++z
#	    if j<(j0-1):#	     channel+=","
#
#
#
#	  if mp_channels_sim.find(channel) == mp_channels_sim.end():#	   mp_channels_sim[channel]=nchannels_sim
#       vchannels_sim.push_back(channel); #lo utilizzo per output more
#	   mp_channels_sim_id[nchannels_sim]=vchannels_sim_id
#       ++nchannels_sim
#
#
#	  path+=to_string(mp_channels_sim[channel])
#	  path+=" "
#
#	 }#end for k
#
#
#	}else:
#
#	  npassi=1
#
#	  channel=""
#	  channel_j=""
#	  for(j=0;j<lrchannels;j++)#	   channel_j=rchannels[j]
#	   channel+=channel_j
#	   vchannels_sim_id[j]=mp_channels[channel_j]
#	   if j<(lrchannels-1):#	     channel+=","
#
#
#
#	  if mp_channels_sim.find(channel) == mp_channels_sim.end():#	   mp_channels_sim[channel]=nchannels_sim
#       vchannels_sim.push_back(channel); #lo utilizzo per output more
#	   mp_channels_sim_id[nchannels_sim]=vchannels_sim_id
#       ++nchannels_sim
#
#
#      path+=to_string(mp_channels_sim[channel])
#	  path+=" "
#
#	}#end else:
#
#    path="0 "+path
#
#  }else{#end order > 1
#
#	path+=" "
#
#
#
#  vy2[i]=path+"e"; #aggiungo lo stato finale
#  ++npassi
#
# }#end for
#
# mp_channels["(conversion)"]=nchannels; #aggiungo canale conversion
# ++nchannels
# vchannels.push_back("(conversion)")
#
# mp_channels["(null)"]=nchannels
# ++nchannels
# vchannels.push_back("(null)")
#
# if order>1:#  mp_channels_sim["(conversion)"]=nchannels_sim
#  vchannels_sim.push_back("(conversion)")
#  for(z=0;z<order;z++)#   vchannels_sim_id[0]=nchannels_sim
#
#  mp_channels_sim_id[nchannels_sim]=vchannels_sim_id
#  ++nchannels_sim
#
#  mp_channels_sim["(null)"]=nchannels_sim
#  vchannels_sim.push_back("(null)")
#  for(z=0;z<order;z++)#   vchannels_sim_id[0]=nchannels_sim
#
#  mp_channels_sim_id[nchannels_sim]=vchannels_sim_id
#  ++nchannels_sim
#
#
#
# if order==1:#  nchannels_sim=nchannels
#
#
# #cout << "Processed 2/4" << endl
#
# ##########################/
# #CREAZIONE DELLE MATRICI FUNZIONALI ALLE SIMULAZIONI
# ##########################
#
# unsigned long int ichannel,ichannel_old,vpi,vci,vni
# string channel_old
#
# npassi=0
#
# Fx S(nchannels_sim,nchannels_sim)
#
# Fx fV(nchannels_sim,l_vui)
#
# for(i=0;i<lvy;i++)#
#  s=vy2[i]
#  s+=" "
#  ssize= (unsigned long int) s.size()
#
#  channel=""
#  channel_old=""
#  ichannel_old=0
#  ichannel=0
#
#  j=0
#  npassi=0
#
#  vci=vc[i]
#  if flg_var_null==1:#   vni=vn[i]
#  }else:
#   vni=0
#
#  vpi=vci+vni
#
#  while(j<ssize)#
#   while(s[j]!=' ')#
#    if j<ssize:#     channel+=s[j]
#
#    j=j+1
#
#
#   if channel.compare(channel_old)!=0:#
#    if(channel[0]!='0'){#se non è il channel start
#
#     if(channel[0]=='e'){ #stato finale
#
#	  ++npassi
#
#	  if(vci>0){ #se ci sono conversion
#	   ichannel=nchannels_sim-2
#	   S.add(ichannel_old,ichannel,vci)
#	   if flg_var_value==1:#		vui=vv[i]/vci
#	    fV.add(ichannel_old,mp_vui[vui],vci)
#
#	   if vni>0:#		goto next_null
#	   }else:
#		goto next_path
#
#
#
#	  if(vni>0){ #se non ci sono conversion
#	   next_null:
#	   ichannel=nchannels_sim-1
#	   S.add(ichannel_old,ichannel,vni)
#	   goto next_path
#
#
#     }else{ #stato non finale
#
#	  if vpi>0:#       ichannel=atol(channel.c_str())
#   	   S.add(ichannel_old,ichannel,vpi)
#
#
#
#
#	 ++npassi
#
#    }else{ #stato iniziale
#
#     ichannel=0
#
#
#
#    channel_old=channel
#    ichannel_old=ichannel
#
#   }#end compare
#
#   channel=""
#
#   j=j+1
#
#  }#end while j<size
#
#  next_path:
#
# }#end for
#
# #out matrice di transizione
#
# List res_mtx
# if out_more==1:#  if order==1:#   res_mtx=S.tran_matx(vchannels)
#  }else:
#   res_mtx=S.tran_matx(vchannels_sim)
#
#
#
#
# #f.r. transizione
# S.cum()
#
# #return(0)
#
# #f.r. conversion value
# if flg_var_value==1:#  fV.cum()
#
#
# #distribuzione numeri uniformi
# double iu,nuf
# nuf=1e6
# NumericVector vunif=runif nuf:
#
# #cout << "Processed 3/4" << endl
#
# #SIMULAZIONI
#
# unsigned long int c,c_last,nconv,max_npassi
# long int id0
# double sval0,ssval
# vector<bool> C(nchannels)
# vector<double> T(nchannels)
# vector<double> V(nchannels)
#
# nconv=0
# sval0=0
# ssval=0
# c_last=0
# iu=0
#
# if max_step==0:#  max_npassi=nchannels_sim*10
# }else:
#  max_npassi=1e6
#
# if nsim==0:#  nsim=1e6
#
#
#
# for(i=0; i<nsim; i++)#
#  c=0
#  npassi=0
#
#  for(k=0; k<nchannels; k++){ #svuoto il vettore del flag canali visitati
#   C[k]=0
#
#
#  C[c]=1; #assegno 1 al channel start
#
#  while(npassi<=max_npassi){ #interrompo quando raggiungo il massimo numero di passi
#
#   if(iu>=nuf){vunif=runif(nuf);iu=0;} #genero il canale da visitare
#   c=S.sim(c,vunif[iu])
#   ++iu
#
#   if(c==nchannels_sim-2){ #se ho raggiunto lo stato conversion interrompo
#    goto go_to_conv
#   }elif(c==nchannels_sim-1){ #se ho raggiunto lo stato null interrompo
#	goto go_to_null
#
#
#   if order==1:#	C[c]=1; #flaggo con 1 il canale visitato
#   }else:
#    for(k=0; k<order; k++)#	 id0=mp_channels_sim_id[c][k]
#	 if id0>=0:#      C[id0]=1
#     }else:
#	  break
#
#
#
#
#   c_last=c; #salvo il canale visitato
#   ++npassi
#
#  }#end while npassi
#
#  go_to_conv:
#
#  if c==nchannels_sim-2){ #solo se ho raggiunto la conversion assegno +1 ai canali interessati (se ho raggiunto il max numero di passi è come se fossi andato a null:
#
#   ++nconv;#incremento le conversion
#
#   #genero per il canale c_last un valore di conversion "sval0"
#   if flg_var_value==1:#    if(iu>=nuf){vunif=runif(nuf);iu=0;
#    sval0=v_vui[fV.sim(c_last,vunif[iu])]
#    ++iu
#
#
#   ssval=ssval+sval0
#
#   for (k=0; k<nchannels; k++)#    if C[k]==1:#	 T[k]=T[k]+1
#	 if flg_var_value==1:#	  V[k]=V[k]+sval0
#
#
#
#
#  }#end if conv
#
#  go_to_null:
#
# }#end for i
#
#
# T[0]=0; #pongo start = 0
# unsigned long int nch0
# nch0=nchannels-3
# T[nchannels-2]=0; #pongo conversion = 0
# T[nchannels-1]=0; #pongo null = 0
#
# double sn=0
# for(i=0;i<lvy; i++)#  sn=sn+vc[i]
#
#
# double sm=0
# for(i=0;i<nchannels-1; i++)#  sm=sm+T[i]
#
#
# vector<double> TV(nch0,0)
# vector<double> rTV(nch0,0)
#
# for (k=1; k<(nch0+1); k++)#  if sm>0:#   TV[k-1]=(T[k]/sm)*sn
#   if(out_more==1){rTV[k-1]=T[k]/nconv;} #removal effects
#
#
#
#
# vector<double> VV(nch0,0)
# vector<double> rVV(nch0,0)
#
# if flg_var_value==1:#
#  V[0]=0; #pongo start = 0
#  V[nchannels-2]=0; #pongo conversion = 0
#  V[nchannels-1]=0; #pongo null = 0
#
#  sn=0
#  for(i=0;i<lvy; i++)#   sn=sn+vv[i]
#
#
#  sm=0
#  for(i=0;i<nchannels-1; i++)#   sm=sm+V[i]
#
#
#  for(k=1; k<(nch0+1); k++)#   if sm>0:#    VV[k-1]=(V[k]/sm)*sn
#    if(out_more==1){rVV[k-1]=V[k]/ssval;} #removal effects
#
#
#
#
#
# vector<string> vchannels0(nch0)
# for(k=1; k<(nch0+1); k++)#  vchannels0[k-1]=vchannels[k]
#
#
# #cout << "Processed 4/4" << endl
#
# if flg_var_value==1:#
#  if out_more==0:#
#   return List.create(Named("channel_name")=vchannels0, Named("total_conversion") = TV, Named("total_conversion_value") = VV )
#
#  }else:
#
#   List res1=List.create(Named("channel_name")=vchannels0, Named("total_conversions") = TV, Named("total_conversion_value") = VV )
#   List res3=List.create(Named("channel_name")=vchannels0, Named("removal_effects_conversion") = rTV, Named("removal_effects_conversion_value") = rVV )
#   return List.create(Named("result") = res1, Named("transition_matrix")=res_mtx, Named("removal_effects") = res3)
#
#
#
# }else:
#
#  if out_more==0:#
#   return List.create(Named("channel_name")=vchannels0, Named("total_conversions") = TV)
#
#  }else:
#
#   List res1=List.create(Named("channel_name")=vchannels0, Named("total_conversions") = TV)
#   List res3=List.create(Named("channel_name")=vchannels0, Named("removal_effects") = rTV)
#   return List.create(Named("result") = res1, Named("transition_matrix")=res_mtx, Named("removal_effects") = res3)
#
#
#
#
#
# END_RCPP
#
#