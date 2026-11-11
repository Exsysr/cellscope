import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scanpy as sc
from provenance import record
 
adata = sc.read_h5ad("out/02_pca.h5ad")
 
# ---- YOUR TURN: how local should the neighbour graph be? ----
N_NEIGHBORS = 15      # k: number of neighbours per cell
N_PCS = 30            # how many principal components define "similar"
# ---------------------------------------------------------------
sc.pp.neighbors(adata, n_neighbors=N_NEIGHBORS, n_pcs=N_PCS, random_state=0)
 
# Try several resolutions and look at what happens to the number and size of clusters
RESOLUTIONS = [0.3, 0.5, 0.8, 1.2]
for res in RESOLUTIONS:
    key = f"leiden_{res}"
    sc.tl.leiden(adata, resolution=res, key_added=key, flavor="igraph",
                 n_iterations=2, directed=False, random_state=0)
    sizes = adata.obs[key].value_counts().to_numpy()
    print(f"resolution {res}: {len(sizes)} clusters, sizes {sizes.tolist()}")
 
# ---- YOUR TURN: choose one resolution (it must be in RESOLUTIONS) and justify it ----
RESOLUTION = 0.8
# ---------------------------------------------------------------------------------------
adata.obs["cluster"] = adata.obs[f"leiden_{RESOLUTION}"].copy()
n_clusters = adata.obs["cluster"].nunique()
print("chosen:", n_clusters, "clusters at resolution", RESOLUTION)
if n_clusters > 12:
    print("WARNING: more than 12 clusters; the palette in Part B only has 12 colours")
 
# Quick look: first PCs coloured by cluster (exploration only, not the final visualisation)
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
codes = adata.obs["cluster"].cat.codes
pcs = adata.obsm["X_pca"]
for ax, (i, j) in zip(axes, [(0, 1), (0, 2)]):
    ax.scatter(pcs[:, i], pcs[:, j], c=codes, cmap="tab20", s=4)
    ax.set_xlabel(f"PC{i + 1}"); ax.set_ylabel(f"PC{j + 1}")
fig.tight_layout()
fig.savefig("out/clusters_pca.png", dpi=120)
 
adata.write_h5ad("out/03_clustered.h5ad")
record("cluster", n_neighbors=N_NEIGHBORS, n_pcs=N_PCS, algorithm="leiden",
       resolution=RESOLUTION, resolutions_tried=RESOLUTIONS, random_state=0,
       n_clusters=int(n_clusters))