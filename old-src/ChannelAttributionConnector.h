#ifndef CHANNELATTRIBUTIONCONNECTOR_H
#define CHANNELATTRIBUTIONCONNECTOR_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct Fx Fx;

Fx* newFx();

void Fx_add(unsigned long int ichannel_old, unsigned long int ichannel, unsigned long int vxi);

void Fx_cum();

unsigned long int Fx_sim(unsigned long int c, double uni);


void deleteFx(Fx* v);

#ifdef __cplusplus
}
#endif

#endif