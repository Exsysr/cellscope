import shutil
import scanpy as sc
from contract import OUT, load_manifest, save_manifest, write_u8, sync_provenance
from provenance import record
 
adata = sc.read_h5ad("out/03_clustered.h5ad")
manifest = load_manifest()
 
# The most important check in the whole project: same cells, same order.
assert adata.n_obs == manifest["n_cells"], \
    f"cell count differs: analysis {adata.n_obs} vs manifest {manifest['n_cells']}. Rerun run_pipeline.py"
 
cl = adata.obs["cluster"]
codes = cl.cat.codes.to_numpy()                      # 0, 1, 2 ... one per cell, in cell order
categories = [str(c) for c in cl.cat.categories]     # code i means cluster categories[i]
 
write_u8("obs_cluster.u8", codes)
manifest["obs"]["cluster"] = {
    "file": "obs_cluster.u8",
    "type": "categorical",
    "categories": categories,
}
 
shutil.copy("out/markers.json", f"{OUT}/markers.json")
manifest["markers"] = "markers.json"
save_manifest(manifest)
 
record("export_clusters", n_clusters=len(categories))
sync_provenance()
print("exported", len(codes), "cell labels,", len(categories), "clusters")