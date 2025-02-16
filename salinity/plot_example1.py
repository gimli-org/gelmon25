#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plotting script for example 1
"""
import numpy as np
import pygimli as pg

def temp_conversion(values, insitu_temp, ref_temp=25, alpha=0.02):
    ret = values / (1 + (insitu_temp - ref_temp) * alpha)
    return ret


# %% Part 1/n: import results
data = pg.DataContainerERT('data.dat')
results = np.load('ert_example1.npz')
mesh = pg.load('paraDomain.bms')

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


# %% Part 3/n: Plotting salinity
plotsalinity = {
    "cMin": 0,
    "cMax": 35,
    "logScale": False,
    "label": "sal (g/l)",
    "cMap": "Spectral_r"
    }

# drawSalinity(cfg, npz, mesh, ax=ax1, date=campaign_date, **kw)
# %% formation factor
# cell midpoints of inversion domain
z_array = pg.y(mesh.cellCenter())

# simple 1D model with 2 values
f_factors = [4.25, 5.56]
f_depth = 13.95

formation = np.ones_like(z_array) * f_factors[0]
formation[z_array < -f_depth] = f_factors[1]

np.savetxt('formation.txt', formation)

# formation = np.loadtxt('formation.txt')
temperature = np.loadtxt('temperature.txt')

vals = temp_conversion(10. / results['model'], temperature)
sal = vals * 0.67 * formation

ax, cbar = pg.show(mesh, data=sal, **plotsalinity)
ax.set_ylim(-30, 4)
# %%
