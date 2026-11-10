import json, os, shutil
import numpy as np
import scanpy as sc
from provenance import record
 
OUT = "../web/public/data"
os.makedirs(OUT, exist_ok=True)
 
adata = sc.read_h5ad("out/02_pca.h5ad")
 
# First three principal components -> positions of the cells
X = adata.obsm["X_pca"][:, :3].astype(np.float64)
center = X.mean(axis=0)
X = X - center
scale = float(np.abs(X).max())        # ONE scale for all axes (see question 4 below)
X = X / scale                         # now every coordinate lies in [-1, 1]
 
X.astype("<f4").tofile(f"{OUT}/emb_pca.f32")      # little-endian float32, N x 3
 
manifest = {
    "contract_version": 1,
    "dataset": "pbmc3k",
    "n_cells": int(adata.n_obs),
    "embeddings": {
        "pca": {"file": "emb_pca.f32",
                "normalisation": {"center": center.tolist(), "scale": scale}}
    },
    "obs": {},
}
with open(f"{OUT}/manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
 
record("export_embedding", name="pca", n_components=3, scale=scale)
shutil.copy("out/provenance.json", f"{OUT}/provenance.json")
print("wrote", adata.n_obs, "cells to", OUT)