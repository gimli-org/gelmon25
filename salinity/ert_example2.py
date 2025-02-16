#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal working example for the pygimli workshop
"""
import numpy as np
import pygimli as pg
from pygimli.physics import ert

# from pygimli.frameworks import PriorModelling, JointModelling, PetroModelling


class transSal(pg.trans.Trans):
    def __init__(self, formation=4, temperature=10, a=0.02, noc=None):
        # super.__init__()
        super(transSal, self).__init__()
        self.formation = formation
        self.temp = temperature
        self.alpha = a

        self.factor = np.ones(noc) * 10. /\
            (1 / 0.6768 * (1 + (temperature - 25) * a) / formation)
        # print('len factor', len(self.factor))
        # sal/0.6768 = mS/cm (fluid 25°C)
        # *(1+(T-25)*a)  (fluid in situ)
        # / formation (bulk)
        # res=10/

    def trans(self, sal):
        res = self.factor / sal
        return res

    def invTrans(self, res):
        sal = self.factor / res
        return sal

    def deriv(self, sal):
        drho_ds = -self.factor / sal**2
        return drho_ds


# %% Part 1/n: Data import and Error Estimation
data = pg.DataContainerERT()
data.load('data.dat')
mesh = pg.load('mesh.bms')

data['err'] = ert.estimateError(
    data,
    relativeError=0.04,
    absoluteUError=5e-5)

# %% Part 2/n: Prior Data Import


# %% Part 3/n: ERT Manager
mgr = ert.ERTManager(data)
mgr.setMesh(mesh)

# %% formation factor
# find cells of inversion domain
which = mesh.cellMarkers() == 2
# cell midpoints of inversion domain
z_array = pg.y(mesh.cellCenter()).array()[which]

# simple 1D model with 2 values
f_factors = [4.25, 5.56]
f_depth = 13.95

formation = np.ones_like(z_array) * f_factors[0]
formation[z_array < -f_depth] = f_factors[1]

# np.savetxt('formation.txt', formation)
# %% temperature
# which = mesh.cellMarkers() == 2
# z_array = pg.y(mesh.cellCenter()).array()[which]
# import src
# from datetime import datetime
# campaign_date = datetime(2022, 12, 5)
# temperature = src.samos.getInsituTemperature(z_array, campaign_date)
# np.savetxt('temperature.txt', temperature)

# formation = np.loadtxt('formation.txt')
temperature = np.loadtxt('temperature.txt')

# pg.show(mgr.paraDomain, data=temperature, cMap='bwr', cMin=0, cMax=20)
# pg.show(mesh)

# %% salinity transformation
salinity_trans = transSal(formation=formation, temperature=temperature)
petro_fop = pg.frameworks.PetroModelling(mgr.fop, salinity_trans)
petro_fop.setMesh(mesh)

# %% import prior data
samos_data = np.loadtxt('samos_data.txt')
samos_pos = np.load('samos_pos.npy')

fluid_data = np.loadtxt('fluid_data.txt')
fluid_pos = np.load('fluid_pos.npy')

# start with zeros 2D positions
pos_vec = np.zeros((0, 2))

# append samos prior data, positions and errors
prior_data = samos_data
prior_error = np.ones_like(samos_data) * 0.2
pos_vec = np.append(pos_vec, samos_pos, axis=0)

# append fluid prior data, positions and errors
pos_vec = np.append(pos_vec, fluid_pos, axis=0)
prior_data = np.append(prior_data, fluid_data)
prior_error = np.append(prior_error, np.ones_like(fluid_data) * 0.05)

# %%
# setup ert prior mesh
# extract paraDomain + make a copy
para_ert = pg.Mesh(petro_fop.paraDomain)

# kick out values of prior outside mesh area
valid = np.ones_like(prior_data, dtype=bool)
for pi, pos in enumerate(pos_vec):
    c = para_ert.findCell(pos)
    if not c:
        valid[pi] = False

pos_vec = pos_vec[valid]
prior_data = prior_data[valid]
prior_error = prior_error[valid]

# setup prior for inversion
prior = pg.frameworks.PriorModelling(para_ert, pos_vec)

# setup inv for prior + petro
fopJoint = pg.frameworks.JointModelling([petro_fop, prior])
fopJoint.setData([data['rhoa'], pg.Vector(prior_data)])
# pg.Vector because the prior vector needs to have
# a size() attribute

# stitch together the data vectors
data_array = np.concatenate((data['rhoa'], prior_data))
error_array = np.concatenate((data['err'], prior_error))

assert len(data_array) == len(error_array)

# %% Part 4/n: Inversion
inv = pg.Inversion(fop=fopJoint, verbose=True)

sal_limits = (0, 40)

inv.dataTrans = pg.trans.TransLog()
inv.modelTrans = pg.trans.TransCotLU(*sal_limits)
inv.setRegularization(1, background=True)

inv.setRegularization(
    2, zWeight=0.1, limits=sal_limits)

model = inv.run(data_array, error_array, startModel=10, lam=20)

# %% Part 5/n: Save model, response and coverage

results = {
    'model': model,
    'coverage': np.ones_like(model),
    'response': inv.response.array(),
    'chi2': inv.inv.getChi2(),
    'rrms': inv.relrms(),
    'error': error_array,
    'pos_vec': pos_vec,
    'prior_data': prior_data
    }
np.savez('ert_example2.npz', **results)
