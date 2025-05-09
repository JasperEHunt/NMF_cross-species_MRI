#! /bin/sh

# Set save path
myPath="/XTRACT/comparison/directory"

# Loop through each number of NMF components to generate correlation matrices
for compNumb in 10 50 60 100 200; do
    python ${myPath}/analysis_scripts/correlateGM.py ${compNumb} ${myPath}/data/NMF_GM_${compNumb}.LR.dscalar.nii ${myPath}/data/merged_xtract.dscalar.nii ${myPath}/results
done
