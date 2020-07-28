# skipped-caipi

## Supporting Jupyter Notebook for "Segmented K-Space Blipped-Controlled Aliasing in Parallel Imaging (Skipped-CAIPI) for High Spatiotemporal Resolution Echo Planar Imaging"

Provisionally accepted by Magnetic Resonance in Medicine, 2020

Rüdiger Stirnberg (1), Tony Stöcker (1,2)

1. German Center for Neurodegenerative Diseases (DZNE), Bonn, Germany
2. Department of Physics and Astronomy, University of Bonn, Bonn, Germany

## Note:

**The provided notebook and functions merely *visualize* skipped-CAIPI sampling.**

**Together with the paper, they may help to reproduce implementation of skipped-CAIPI sampling on your MRI scanner platform.**

## Jupyter notebook (index.ipynb)

Run this jupyter notebook to visualize blipped-CAIPI, shot-selective or skipped-CAIPI EPI sampling of any CAIPIRINHA pattern specified.

**Don't have jupyterlab/ jupyter notebook installed? Run it online:**

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mrphysics-bonn/skipped-caipi/338eeef228515ea7216536ca30bfc3d16ed71aa6?filepath=index.ipynb)

In one of the first cells, you can specify the CAIPI pattern parameters and a segmentation factor.

In the following cells, you will be presented plots and get informed about the z-blips and z-blip cycle of:

* the blipped-CAIPI trajectory associated to the CAIPI pattern
* the skipped-CAIPI trajectory associated to the CAIPI pattern, given the specified segmentation factor

alongside the corresponding Equations.

In the last cell, all unique trajectories associated to specified CAIPI pattern are plotted, thus reproducing Supporting Information Figure S2.

## Helper functions (skippedcaipi.py)

Functions used by the jupyter notebook to calculate z-blips and z-blip cycles and to visualize elementary sampling cells and superimposed phase encoode trajectories.

Comments (in particular of the 'get_trajectory_indices' function) may help to reproduce skipped-CAIPI sampling on your MRI scanner platform, or simply appreciate that skipped-CAIPI can simply be understood as both:

* segmentation applied along the blipped-CAIPI trajectory associated to the CAIPI pattern, or
* a CAIPI shift introduced into traditional segmented EPI
