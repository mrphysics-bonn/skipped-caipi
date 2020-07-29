#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""skippedcaipi.py: Helper functions for Supporting Jupyter Notebook (index.ipynb) for

"Segmented K-Space Blipped-Controlled Aliasing in Parallel Imaging (Skipped-CAIPI) for High Spatiotemporal Resolution Echo Planar Imaging"

Provisionally accepted by Magnetic Resonance in Medicine, 2020

Rüdiger Stirnberg (1), Tony Stöcker (1,2)

1. German Center for Neurodegenerative Diseases (DZNE), Bonn, Germany
2. Department of Physics and Astronomy, University of Bonn, Bonn, Germany

"""

__author__ = "Rüdiger Stirnberg, Tony Stöcker"
__maintainer__ = "Rüdiger Stirnberg"
__email__ = "ruediger.stirnberg@dzne.de"
__version__ = "1.0"

import numpy as np
import matplotlib.pyplot as plt

# Eq. A1:
def get_zblips(Ry, Rz, Dz, S):
    bz1 = np.mod(S*Dz,Rz)
    bz2 = np.mod(Rz-bz1, Rz)
    return int(bz1), int(bz2)

# Eq. A2:
def get_zblipcycle(Rz, bmin):
    if bmin==0:
        ns = 1
    elif np.mod(Rz,bmin)==0:
        ns = Rz/bmin
    else:
        ns = Rz
    return int(ns)

# Breuer FA, Blaimer M, Mueller MF, et al. Controlled aliasing in volumetric parallel imaging (2D CAIPIRINHA). Magnetic Resonance in Medicine 2006:
def elementary_sampling(Ry, Rz, Dz, repeat=0):
    R = Ry*Rz
    cell = np.zeros((R,R), dtype=bool)

    for i,col in enumerate(range(0,R,Ry)):
        cell[np.mod(i*Dz+np.arange(0,R,Rz), R), col] = True

    if repeat>0:
        cell = np.tile(cell, [1, repeat+1])

    return cell

# Implement skipped-CAIPI segmenation of blipped-CAIPI trajectory for plotting purposes:
def get_trajectory_indices(cell, segmentation, shot=0):
    # Deduce acceleration factors from elementary sampling cell
    R = cell.shape[1]
    Rz = np.diff(np.argwhere(cell[:,0]).flatten())
    if Rz.size==0:
        Rz = R
    else:
        Rz = Rz[0]

    # Consider only partition indices in [0, Rz) along z in the elementary cell
    # (there are no partitoin indices >= Rz on the blipped-CAIPI traectory of the first shot)
    partseg = cell[:Rz,:]
    indices = np.argwhere(partseg)

    # Sort ascending according to primary phase encode indices -> blipped-CAIPI trajectory
    indices = indices[indices[:,1].argsort()]

    # Return only every "segementation"th index starting at "shot"th index -> skipped-CAIPI trajectory
    indices = indices[shot::segmentation]
    return indices


# Helper function to color axis spines:
def color_axis_spines(color, ax=None):
    if not ax:
        ax = plt.gca()

    spines = ax.spines.values()
    for s in spines:
        s.set_color(color)
        s.set_linewidth(2)

# Helper function to plot the phase encode trajectory between samples.
# As the y- and z-gradient blips are triangular, the k-space trajectory (integral) is a parabola:
def plot_parabola_connection(xy1, xy2, axis=None, num=10, bRotate=False, **kwargs):
    if axis==None:
        axis=plt.gca()

    dx = xy2[0]-xy1[0]
    dy = xy2[1]-xy1[1]
    x = np.linspace(xy1[0], xy2[0], num+1, endpoint=True)

    x1 = x[:num//2]
    x2 = x[num//2:]

    a = 2*dy/dx**2
    y1 = a * (x1-xy1[0])**2 + xy1[1]
    y2 = -a *(x2-xy2[0])**2 + xy2[1]
    y = np.append(y1, y2)

    if not bRotate:
        p = axis.plot(x,y,**kwargs)
    else:
        p = axis.plot(y,x,**kwargs)

    return p

# Plot elementary sampling cell (optionally repeated along y and optionally rotated by 90 degrees)
# and superimpose the sampling trajectory of the first shot using specified color
# (and optinally the trajectories of S-1 following shots using dadrker colors and thiner lines):
def plot_skipped_caipi(Ry, Rz, Dz, S, ax=None, color=None, repetitions=0, bAllShots=False, bRotate=False):
    if ax==None:
        ax = plt.gca()

    colors = ['w', 'k', 'r', 'g', 'b']
    pattern = elementary_sampling(Ry,Rz,Dz,repetitions).astype(int)

    if bRotate:
        pat = np.fliplr(np.rot90(pattern,3))
    else:
        pat = pattern

    ax.pcolor(pat+0.3 , cmap='gray', linestyle='-', edgecolor=[0.2, 0.2, 0.2], lw=0.75, vmin=0, vmax=1.0)


    shotidx = get_trajectory_indices(pattern, S, 0)

    if color is not None:
        for si in range(shotidx.shape[0]-1):
            plot_parabola_connection(shotidx[si,::-1]+0.5, shotidx[si+1,::-1]+0.5, axis=ax, num=11, color=color, lw=1, bRotate=bRotate)
        ax.scatter(shotidx[:,1-int(bRotate)]+0.5, shotidx[:,0+int(bRotate)]+0.5, color=color, edgecolor=color, s=4, zorder=3)
        ax.scatter(shotidx[:,1-int(bRotate)]+0.5, shotidx[:,0+int(bRotate)]+0.5, color='w', edgecolor=color, s=0.5, zorder=3, linewidth=0)

        if bAllShots:
            col = np.array(color, dtype=float)
            delta_off = 0.0#0.1
            for s in range(1,S):
                col /= float(2+s/S)
                shotidx = get_trajectory_indices(pattern, S, s)
                off = np.array([0.0, (-1)**(s) * delta_off * ((s+1)//2)])
                for si in range(shotidx.shape[0]-1):
                    plot_parabola_connection(shotidx[si,::-1]+off+0.5, shotidx[si+1,::-1]+off+0.5, axis=ax, num=11, color=col.copy(), lw=0.5, ls='-', bRotate=bRotate)
                ax.scatter(shotidx[:,1-int(bRotate)]+0.5, shotidx[:,0+int(bRotate)]+0.5, color=col.copy(), s=0.5, zorder=3)

    ax.set_aspect(1.0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.invert_yaxis()
    if Dz<0:
        Dsign='-' # Symbol for negative CAIPI shift
    else:
        Dsign='' # Symbol for positive or zero CAIPI shift
    label = r'$%d\cdot{%d \times %d}_{%sz%d}$' % (S, Ry, Rz, Dsign, np.abs(Dz))

    return ax, label
