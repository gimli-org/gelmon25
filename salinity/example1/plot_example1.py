#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plotting script for example 1
"""
import numpy as np
import pygimli as pg

# %% Part 1/n: import results
data = pg.DataContainerERT('data/short.dat')
results = np.load('results/ert_example1.npz')
mesh = pg.load('results/mesh_example1.bms')

# %% Part 2/n: Plotting the model
plotmodel = {
    "label": "EC$_b$ (mS/cm)",
    "logScale": False,
    "cMin": 0,
    "cMax": 12,
    "cMap": "Spectral_r",
    "colorBar": True
    }

ax, cbar = pg.show(mesh, data=10./results['model'], **plotmodel)
ax.set_ylim(-30, 4)

# %% Part 3/n: Plotting misfit
plotmisfit = {
    "cMap": "bwr",
    "cMin": -4,
    "cMax": 4,
    "label": "error weighted misfit",
    "colorBar": True
    }

misfit = (np.log(data['rhoa']) - np.log(results['response'])) / results['error']
ax, cbar = pg.show(data, data=misfit, **plotmisfit)
