# それぞれの系列について、パラメータを求め直す。

import matplotlib.pyplot as plt
import numpy as np
import glob 
import pandas as pd
import seaborn as sns
import scipy

from Function import synthetic
from Function import original_model

case = 1

# 大地震のリストの読み込み
dat_LEQ = pd.read_csv('./../LEQ_analysis/case'+str(case)+'/case'+str(case)+'_foreshocks.csv',index_col = 0)

# 解析対象となる地震のEQidのみを抽出
EQid = dat_LEQ.index
EQid_list = []
for i in range(len(EQid)):
    new_EQid = f'{EQid[i]:03}'
    EQid_list.append(new_EQid)


success_list = []
for EQid in EQid_list[:]:
    
    dir = './../LEQ_analysis/case'+str(case)+'/LEQ_'+EQid+'/'
    print('alalyzed dir is ' ,dir)
    # Read eartquake catalog
    data_file = dir+'/'+EQid+'_all_EQ_dat_foreshocks.csv'
    preslip_dat = pd.read_csv(data_file, index_col=0)

    preslip_dat = preslip_dat[preslip_dat['Magnitude']>=2.5].reset_index(drop=True)

    # 時間とマグニチュードの情報だけを取り出す
    #preslip_dat = preslip_dat[['d_dates','Magnitude']]    
    ti = np.array(preslip_dat['d_dates'])
    Mi = np.array(preslip_dat['Magnitude'])

    # -----limit Magnitude & time information -----
    M0 = 2.5
    
    ts = preslip_dat['d_dates'].iloc[0]
    T = preslip_dat['d_dates'].iloc[len(preslip_dat['d_dates'])-1]
    Teq = preslip_dat['d_dates'].iloc[len(preslip_dat['d_dates'])-1]

    # ----- parameters from Okutani (2011),table2 B0s02007 single-----
    #mu,K,a,c,p = 0.05, 0.019, 0.2, 0.05, 1.09
    mu= 1.2890247150365962
    K= 0.1847169833637205
    a= 0.754763052903735
    c= 0.0607192347745827
    p= 1.0780766258111925

    # difine initial parameter for each model
    param_ini_ori = np.array([mu,K,a,c,p])

    # ----- paramter optimize -----
    #parameter = mu[0],K[1],L[2],a[3],c[4],d[5],p[6],q[7]
    result_ori = scipy.optimize.minimize(fun=original_model.minuslogL_ori, x0=param_ini_ori, args=(Mi,M0,ti,Teq) ,method='Powell')
    param_ori = result_ori.x

    ### パタメータの保存　### 
    param_index_ori = ['mu','K','a','c','p']

    # preslip model のパラメータ保存
    data_ori = pd.DataFrame(index = param_index_ori)
    data_ori['param'] = param_ori
    print(data_ori)
    data_ori.to_csv(dir+'original_para_new.csv',index=True)