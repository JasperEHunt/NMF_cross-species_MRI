#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 14:09:00 2024

@author: Jasper E. Hunt

CorrelateGM is a tool for calculating the correlations between NMF GM components and tract blueprints identified through traditional atlas-based tractography. Supply two scalar CIFTI files (*.dscalar.nii), and the tool will produce a correlation matrix between every NMF GM component and every tract's blueprint, allowing the user to determine which component(s) are best correlated with each tract.

CorrelateGM requires the following libraries:
    sys, numpy, scipy, nibabel, matplotlib, seaborn

Usage:
python correlateGM.py <n_components> <NMF_WG_path> <atlas_tractography_path> <save_directory>

Compulsory arguments:
	<n_components> - number of NMF components
	<NMF_GM_path> - path to file containing NMF grey matter components
	<atlas_tractography_path> - path to file containing blueprints of tracts identified using atlas-based tractography
    <save_directory> - directory in which to save output files

Example run:
> python correlateGM.py 50 '${NMFpath}/NMF_GM_50.nii.gz' '${XTRACTpath}/myBlueprint.LR.dscalar.nii' '${analysisPath}/results'

CorrelateGM outputs two files:
	- A .csv file containing the correlation matrix. Each column represents the blueprint of a tract identified via atlas-based tractography. Each row represents an NMF GM component.
	- A .png file containing a graphical representation of the correlation matrix.
"""

# Load required libraries, output helpful message if libraries are missing
try:
    import sys
    import numpy as np
    import nibabel as nib
    import matplotlib.pyplot as plt
    import seaborn as sns
    print("Required libraries are installed.")
except:
    print("One or more libraries is missing. This script requires 'sys', 'numpy', 'scipy', 'nibabel', 'matplotlib', and 'seaborn'.")

# Function which computes a matrix of correlations between NMF and XTRACT components
def correlateGM(nmf,xtract):
    n_tracts = np.shape(xtract)[0]
    n_comp = np.shape(nmf)[0]
    corrmat = np.empty((n_tracts, n_comp))
    for i in range(n_tracts):
        for j in range(n_comp):
            corrmat[i,j] = np.corrcoef(xtract[i,:], nmf[j,:])[0,1]
    return corrmat
    
# User arguments
n_components = sys.argv[1] # user-entered number of NMF components
NMF_GM_path = sys.argv[2] # path to DScalar GIFTI file containing NMF GM components
atlas_tractography_path = sys.argv[3] # path to DScalar GIFTI file containing atlas-derived GM components
save_directory = sys.argv[4] # directory in which to save output files

# Load in CIFTI files
NMF_components = nib.loadsave.load(NMF_GM_path).get_fdata()
atlas_tracts = nib.loadsave.load(atlas_tractography_path).get_fdata()

# Display warning if the user's entered number of components does not match the number of components in the NMF_GM file
if int(n_components) != NMF_components.shape[0]:
    print("Warning: user-entered number of components does not match shape of the NMF GM components file. Are you sure your NMF file has " + str(n_components) + " components?")

# Generate an array of correlations where each row is an NMF component and each column is an atlas-derived component
print("Calculating correlations...")
corrs = correlateGM(NMF_components,atlas_tracts)
print("Done!")

# Save output as .csv
print("Saving correlation matrix in .csv format")
np.savetxt(save_directory + "/" + str(n_components) + "_NMF_GM_correlation.csv", corrs, delimiter=",")

# Save output as a plot
print("Saving matrix graphic")
# Determine an appropriate height for the plot
heightWidthRatio = NMF_components.shape[0] / atlas_tracts.shape[0]
plotHeight = round(heightWidthRatio * 10)

# Generate the plot using Seaborn
plt.figure(figsize=(10, plotHeight))
graphicOut = sns.heatmap(corrs, linewidth=0.25, cmap='plasma', xticklabels=True, yticklabels=True,)
graphicOut.set_xlabel('Atlas component')
graphicOut.xaxis.tick_top()
graphicOut.xaxis.set_label_position('top')
graphicOut.set_ylabel('NMF component')
plt.savefig(save_directory + "/" + str(n_components) + "_NMF_GM_correlation.png")
