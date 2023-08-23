#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import numpy as np
from tqdm import tqdm
import matplotlib
matplotlib.use('webagg')
from matplotlib import pyplot as pl
import os


x = 'pickles/Abundance_with_PAHs/clump_0_reordered.pkl'
l = 'pickles/Abundance_with_PAHs/clump_0_reordered.struct'
ctr = 'pickles/model_control_simulation/model_control_simulation_0.pkl'
ctr2 = 'pickles/model_control_simulation/model_control_simulation_0.struct'
#x = 'pickles/indiv_particles/clump_11_reordered.pkl'

y = 'correction_sur_abondances.txt'
corr = {}
f = open(y,'r')
f.readline()
for ligne in f:
    if ligne[0] != '!':
        mots = ligne.split()
        a = mots[0]
        b = float(mots[1])
        c = float(mots[2])
        d = float(mots[3])
        corr[a] = d
    

h = 'Abondances_observees.txt'
obs = {}
ob = []
pas_ob =[]
nautilus_error = []
val = []
f = open(h,'r')
f.readline()
f.readline()
for ligne in f:
    if ligne[0] != '!':
        mots = ligne.split()
        a = mots[0]
        b = float(mots[3])
        obs[a] = b
        val.append(b)
    if ligne[0] == '!':
        mots = ligne.split()
        a = mots[0]
        a1 = a[1::]
        b = mots[1]
        c = mots[2]
        if b[0] == '<':
            pas_ob.append(a1)
        elif c[0] == '<':
            pas_ob.append(a1)
        else:
            nautilus_error.append(a1)
val = list(np.sort(val)[::-1])
for i in val:
    for spec in obs:
        ab = obs[spec]
        if ab == i:
            if spec not in ob:
                ob.append(spec)


#pl.ion()
with open('{}'.format(x),'r') as f:
    ab = pickle.load(f)
with open('{}'.format(l),'r') as g:
    struct = pickle.load(g)
with open('{}'.format(ctr),'r') as b:
    ctrl = pickle.load(b)
with open('{}'.format(ctr2),'r') as a:
    cstruct = pickle.load(a)
    
speclist = [i for i in ob[0:4]]
speclist.append('C+')
colors = ['g','b','orange','grey','r']

pl.figure()
pl.clf()
for ispec, specname in tqdm(enumerate(speclist)):
    for iab, abundance in tqdm(enumerate(ab[specname])):
        if iab == 0:
            pl.plot(ab['time'],np.log10(abundance),color=colors[ispec],label=specname,alpha=0.3)
        else:
            pl.plot(ab['time'],np.log10(abundance),color=colors[ispec],alpha=0.1)
    maxAb = -100  # -100 =max or 0 =min
    m = []
    for abondance in ab[specname]:
        k = np.argmax(abondance)
        m.append(k)
        lgab =np.log10(abondance)
        if np.any(lgab >= maxAb):
            maxAb = lgab
    print 'max Abondance',specname,' =', max(maxAb)
    #print 'min Abondance C+ =', min(minAb)
    #print 'Average index =', np.mean(m)
    
pl.legend(loc=0)
pl.xlabel('Time in years')
pl.ylabel('Log(Abundance)')
pl.xlim(4e7,5e7)
pl.title('Abundance against time')
#pl.pause(4)

q = np.median(ab['C+'],axis=0)
#print q
s = np.argmin(q)

pl.figure()
pl.clf()
z = []
for ispec, specname in tqdm(enumerate(corr.keys())):
    z.append(np.fabs(np.log10(ab[specname])-np.log10(corr[specname])))
    
z = np.array(z)
dod = np.sum(z,axis=0)/len(z)

for d in dod:
    pl.plot(ab['time'],d,'k',alpha=0.1)
  
pl.title('Average dod against time')
pl.xlabel('Time in years')
pl.ylabel('distance of disagreement')
pl.xlim(4e7,5e7)
#pl.pause(4)

fig3 = pl.figure()
fig3.clf()
ax = fig3.add_axes([0.1, 0.1, 0.6, 0.8])
zm = []
for ispec, specname in tqdm(enumerate(corr.keys())):
    zm.append(np.fabs(np.log10(ctrl[specname])-np.log10(corr[specname])))
    
zm = np.array(zm)
do = np.sum(zm,axis=0)/len(zm)
sm = np.argmin(do)
ti = ctrl['time']
gt = ti[sm]
t1 = '{:.1E}'.format(np.around(gt))
gj = cstruct['Tgrain']
t4 = np.mean(gj[:,sm])
hj = cstruct['Tgas']
t3 = np.mean(hj[:,sm])
jj = cstruct['Av']
t5 = '{:.3}'.format(np.mean(jj[:,sm]))
kj = cstruct['H2_density']
t2 = '{:.3E}'.format(np.around(np.mean(kj[:,sm])))

for d in do:
    ax.plot(ctrl['time'],d,'k')
  
ax.set_title('Average model dod against time')
ax.set_xlabel('Time in years')
ax.set_ylabel('distance of disagreement')
#ax.set_xlim(4e7,5e7)
fig3.text(0.72,0.5,' \n Best time = {} yrs  \n H2 density = {} part/cm-3 \n Tgas = {} K \n Tgrain = {} K \n Visual extinction = {} mag'.format(t1,t2,t3,t4,t5),fontsize='x-small',bbox=dict(facecolor='white',edgecolor='black'))
#pl.pause(4)

fig,(ax1, ax2, ax3, ax4) = pl.subplots(4,1,sharex=True)
im = []
jm = []
km = []
ibm = []
for it , i in enumerate(struct['Tgas'][0]):
    im.append(np.median(struct['Tgas'][:,it]))
im = np.array(im)
for jt , j in enumerate(struct['Tgrain'][0]):
    jm.append(np.median(struct['Tgrain'][:,jt]))
jm = np.array(jm)
for kt , k in enumerate(struct['H2_density'][0]):
    km.append(np.median(struct['H2_density'][:,kt]))
km = np.array(km)
for ibt , ib in enumerate(struct['Av'][0]):
    ibm.append(np.median(struct['Av'][:,ibt]))
ibm = np.array(ibm)
    
for it,i in enumerate(struct['Tgas']):
    if it ==0:
        ax1.plot(ab['time'],i,alpha=0.1,color='k',label='Tgas')
    else:
        ax1.plot(ab['time'],i,alpha=0.1,color='k')
ax1.plot(ab['time'],im,label='Moyenne Tgas',color='purple')
for jt,j in enumerate(struct['Tgrain']):
    if jt ==0:
        ax2.plot(ab['time'],j,alpha=0.1,color='k',label='Tgrain')
    else:
        ax2.plot(ab['time'],j,alpha=0.1,color='k')
ax2.plot(ab['time'],jm,label='Moyenne Tgrain',color='purple')
for kt,k in enumerate(struct['H2_density']):
    if kt ==0:
        ax3.plot(ab['time'],np.log10(k),alpha=0.1,color='k',label='H2_density')
    else:
        ax3.plot(ab['time'],np.log10(k),alpha=0.1,color='k')
ax3.plot(ab['time'],np.log10(km),label='Moyenne H2_density',color='purple')
for ibt, ib in enumerate(struct['Av']):
    if ibt ==0:
        ax4.plot(ab['time'],ib,alpha=0.1,color='k',label='Av')
    else:
        ax4.plot(ab['time'],ib,alpha=0.1,color='k')
ax4.plot(ab['time'],ibm,label='Moyenne Av',color='purple')

ax1.set_title('Temperature of gas against time',fontsize='x-small')
ax1.set_ylabel('Tgas in K',fontsize='small')
ax1.legend(loc=0)
ax1.set_ylim(0,200)

ax2.set_title('Temperature of grain against time',fontsize='x-small')
ax2.set_ylabel('Tgrain in K',fontsize='small')
ax2.legend(loc=0)

ax3.set_title('Log H2 density against time',fontsize='x-small')
ax3.set_ylabel('Log (H2 density in part/cm-3)',fontsize='x-small')
ax3.legend(loc=0)

ax4.set_title('Extinction visual against time',fontsize='x-small')
ax4.set_ylabel('Av in mag',fontsize='small')
ax4.legend(loc=0)

fig.text(0.5, 0.96, 'Parameters against time', ha='center', fontsize='large')
fig.text(0.5, 0.04, 'Time in years', ha='center',fontsize='large')
#pl.pause(4)

idx_time =[s-50,s-5,s,s+5]
u = len(idx_time)
fig2, a = pl.subplots(1,u,sharex=True)
a = a.ravel()
ti = ab['time']
bt = ti[s]

for t in idx_time:
    it = idx_time.index(t)
    ax = a[it]
    if t == s:
        for ispec, specname in tqdm(enumerate(speclist)):
            abundance = ab[specname]
            bundance = ctrl[specname]
            ax.hist(np.log10(abundance[:,t]),label=specname,color=colors[ispec],orientation='horizontal',alpha=0.2)
            ax.plot(80,np.log10(bundance[:,sm]),linestyle=' ',marker='o',label='control {}'.format(specname),color=colors[ispec])
            w = np.mean(np.log10(abundance[:,t]))
            n = np.log10(obs[specname])
            #print w
            
            ax.axhline(y=w,color=colors[ispec],linestyle=':')
            ax.axhline(y=n,color=colors[ispec])
            
            v1 = '{:.1E}'.format(np.around(bt))
            gi = struct['Tgrain']
            v4 = np.mean(gi[:,t])
            hi = struct['Tgas']
            v3 = np.mean(hi[:,t])
            ji = struct['Av']
            v5 = '{:.3}'.format(np.mean(ji[:,t]))
            ki = struct['H2_density']
            v2 = '{:.3E}'.format(np.around(np.mean(ki[:,t])))
            
            ax.set_title('best time = {} yrs \n H2 density = {} part/cm-3 \n Tgas = {} K \n Tgrain = {} K \n Visual extinction = {} mag'.format(v1,v2,v3,v4,v5),fontsize='x-small')
            ax.set_ylim(-20,-3)
            ax.set_xlim(0,100)
            ax.legend(loc=0)
    else:
        for ispec, specname in tqdm(enumerate(speclist)):
            abundance = ab[specname]
            ax.hist(np.log10(abundance[:,t]),color=colors[ispec],orientation='horizontal',alpha=0.2)
        
            w = np.mean(np.log10(abundance[:,t]))
            #print w
            ax.axhline(y=w,color=colors[ispec],linestyle=':')
            tot = ti[t]-bt
            
            v = '{:.0E}'.format(np.around(tot))
            if tot >= 0:
                ax.set_title('best time +{}'.format(v), fontsize='small')
            else:
                ax.set_title('best time {}'.format(v), fontsize='small')
            
            ax.set_ylim(-20,-3)
            ax.set_xlim(0,100)
            ax.legend(loc=0)
fig2.text(0.5, 0.96, 'Propability density', ha='center', fontsize='medium')
fig2.text(0.04, 0.5, 'Log(Abondance)', va='center', rotation='vertical')
fig2.text(0.5, 0.04, 'Number of models', ha='center')
#pl.pause(4)

#idx_time = 200
#speclist = ['CO','JCO','KCO','C','C+']
#pl.figure()
#pl.clf()
#for ispec, specname in tqdm(enumerate(speclist)):
    #abundance = ab[specname]
    #pl.hist(abundance[:,idx_time])
 
