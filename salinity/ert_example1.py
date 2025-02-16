#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal working example for the pygimli workshop
"""
import numpy as np
import pygimli as pg
from pygimli.physics import ert


# %% Part 1/5: Data import
data = pg.DataContainerERT()
data.load('data.dat')
# pg.show(data)

# %% Part 2/5: Estimate error
data['err'] = ert.estimateError(
    data,
    relativeError=0.04,
    absoluteUError=5e-5)

data.show('err')

# %% Part 3/5: ERT Manager
mgr = ert.ERTManager(data)

mesh_param = {'paraMaxCellSize': 10,
              'quality': 34.4,
              'paraDepth': 60,
              'paraDX': 0.25
              }

mesh = mgr.createMesh(**mesh_param)
mgr.setMesh(mesh)
pg.show(mgr.paraDomain)
# pg.show(mesh)

# %% Part 4/5: Inversion
mgr.inv.setRegularization(2, zWeight=0.1)
inv_param = {'lam': 100,
             'startmodel': np.median(data["rhoa"])}
mgr.invert(**inv_param)

# %% Part 5/5: Save model, response and coverage
results = {
    'model': mgr.model.array(),
    'coverage': mgr.coverage(),
    'response': mgr.inv.response.array(),
    'chi2': mgr.inv.inv.getChi2(),
    'rrms': mgr.inv.relrms(),
    'error': data['err']
    }
np.savez('ert_example1.npz', **results)
mgr.paraDomain.save('paraDomain.bms')
mgr.mesh.save('mesh.bms')