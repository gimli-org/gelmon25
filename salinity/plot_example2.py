#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal working example for the pygimli workshop
"""
import numpy as np
import pygimli as pg

# %% Import results
data = pg.DataContainerERT('data.dat')
results = np.load('ert_example2.npz')
mesh = pg.load('paraDomain.bms')

# %% Plotting misfit
plotmisfit = {
    "cMap": "bwr",
    "cMin": -4,
    "cMax": 4,
    "label": "error weighted misfit",
    "colorBar": True
    }

misfit = (np.log(data['rhoa']) - np.log(results['response'][:data.size()])) / results['error'][:data.size()]
ax, cbar = pg.show(data, data=misfit, **plotmisfit)

# %% Plotting the model
plotsalinity = {
    "cMin": 0,
    "cMax": 35,
    "logScale": False,
    "label": "sal (g/l)",
    "cMap": "Spectral_r"
    }

import matplotlib

ax, cbar = pg.show(mesh, data=results['model'], **plotsalinity)
ax.set_ylim(-30, 4)

cmap = matplotlib.cm.get_cmap(plotsalinity['cMap'])
norm = matplotlib.colors.Normalize(
    vmin=plotsalinity['cMin'],
    vmax=plotsalinity['cMin'])


asdfasdf

ax.

for vi, val in enumerate(results['prior']:
    kw['facecolor'] = cmap(norm(val[tag]))
    ax.add_patch(Rectangle(
        (val['xpos'] - width/2,
            -val['depth'] - height/2),
        width, height, **kw))