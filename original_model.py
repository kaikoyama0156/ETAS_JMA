##### ETAS original model function #####
from numba import jit
import numpy as np
@jit
def ramda_ori(param,Mi,M0,t,ti,Teq):
    mu,K,a,c,p = param
    ramda_t = mu 
    
    for i in range(len(ti)):
        if(ti[i]<t):
            ramda_t += K*np.exp(a*(Mi[i]-M0)) / ((t-ti[i]+c)**p)
    return ramda_t

# -----integral of ramda(t)-----
@jit
def integral_ramda_ori(param,Mi,M0,ti,Teq):
    mu,K,a,c,p = param
    sum_ramda = mu*Teq
    # Teqまで計算
    for i in range(len(ti)):
        # 0 ~ len(ti)-1　まで計算、つまり、ti[len(ti)-1] = Teqまで計算
        # calculate 0 ~ Teq
        sum_ramda += -K/(p-1)*((np.exp(a*(Mi[i]-M0)))*((Teq-ti[i]+c)**(1-p))) + K/(p-1)*((np.exp(a*(Mi[i]-M0)))*(c**(1-p))) 
        #sum_ramda += -K/(p-1)*((np.exp(a*(Mi[i]-M0)))*((Teq-ti[i]+c)**(1-p))) + K/(p-1)*((np.exp(a*(Mi[i]-M0)))*(c**(1-p))) 
    return sum_ramda


# ----- calc logL ----------
@jit
def logL_ori(param, Mi,M0,ti,Teq):
    calc = 0
    # exclude Teq for calculation of sigma
    for t in ti[1:]:
        # ti=Teq-1まで計算
        # →最後まで計算
        calc += np.log(ramda_ori(param,Mi,M0,t,ti,Teq))
    return calc - integral_ramda_ori(param,Mi,M0,ti,Teq)

# ----- prior condition ,-log_L -----
@jit
def minuslogL_ori(param, Mi,M0,ti,Teq):
    mu,K,a,c,p = param
    # --- parameters should be positive ---
    ### add new condition d<100, q<10 ###
    if(mu<=0 or K<=0 or a<=0 or c<=0 or p<=1.0):
        return np.inf
    else:
        return (-1)*logL_ori(param,Mi,M0,ti,Teq)
    return sum_ramda

# ----- calc AIC ----------
@jit
def AIC_ori(minuslogL_ori):
    # the numbers of free parameter 
    k = 5
    return 2*minuslogL_ori + 2*k