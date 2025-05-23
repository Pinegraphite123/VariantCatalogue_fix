#!/usr/bin/env python

import hail as hl
import sys
import os

temp_directory=sys.argv[2]
hl.init(tmp_dir=temp_directory, default_reference='GRCh38')

pca_loadings = hl.read_table(sys.argv[4])
sarek_mt = hl.import_vcf(sys.argv[1], reference_genome='GRCh38', array_elements_required=False)
#pca_loadings.describe()
#sarek_mt.describe()

import onnx
from gnomad.sample_qc.ancestry import (
    apply_onnx_classification_model,
    assign_population_pcs,
)


onnx_rf = sys.argv[5]

with hl.hadoop_open(onnx_rf, "rb") as f:
    onx_fit = onnx.load(f)


pcs = hl.experimental.pc_project(sarek_mt.GT, pca_loadings.loadings, pca_loadings.pca_af)

ht, model = assign_population_pcs(
    pcs,
    pc_cols=pcs.scores[:20], # define number of pc, depend on the loaded model
    fit=onx_fit,
    # Using a low min_prob (like 0.01) is permissive: almost everyone gets a label. 
    # High values (e.g. 0.9) are conservative: only very confident calls are made.
    min_prob=0.01, 
    apply_model_func=apply_onnx_classification_model,
)


ht.aggregate(hl.agg.counter(ht.pop))



# Extract the first two PCs and population labels
# Plot results for population assignment in pca
p = hl.plot.scatter(ht.pca_scores[0], ht.pca_scores[1],
                    label=ht.pop,
                    title='PCA', xlabel='PC1', ylabel='PC2',
                    n_divisions=None)

export_png(p, filename="pca_plot.png")





