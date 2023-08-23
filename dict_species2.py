#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import os
import numpy as np


nom_global = 'Abundance_with_PAHs'
m = os.listdir(nom_global)

for i in m:
    dossier = '{}/{}/0'.format(nom_global,i)
    filelist = os.listdir('{}/ab'.format(dossier))
    especes = {}
    for fn in filelist:
        if fn != '.DS_Store':
            specname = os.path.splitext(fn)[0]
            especes[specname] = []
    dossier2 = '{}/{}'.format(nom_global,i)
    dirlist = os.listdir(dossier2)
    for dirname in dirlist:
        if os.path.isdir('{}/{}'.format(dossier2,dirname)):
            filelist = os.listdir('{}/{}/ab'.format(dossier2,dirname))
            for fn in filelist:
                if fn != '.DS_Store':
                    data = np.loadtxt('{}/{}/ab/{}'.format(dossier2,dirname,fn),comments='!')
                    specname = os.path.splitext(fn)[0]
                    especes[specname].append(data[:,1])
                    especes['time'] = data[:,0]
    for specname in especes.keys():
        especes[specname] = np.array(especes[specname])
    pkl_dir = 'pickles'
    with open('{}/{}/{}.pkl'.format(pkl_dir,nom_global,i),'wb') as f:
        pickle.dump(especes,f)
            
#with open('{}.pkl'.format(dossier2),'rb') as f:
    #especes = pickle.load(f)