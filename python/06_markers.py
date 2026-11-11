import json
import scanpy as sc
from provenance import record
 
adata = sc.read_h5ad("out/03_clustered.h5ad")
 
TOP_N = 15
 
# Wilcoxon rank-sum test, one cluster against all the others, for every gene.
# use_raw=True: test on ALL genes (log-normalised), not only the 2000 variable genes used for PCA.
sc.tl.rank_genes_groups(adata, groupby="cluster", method="wilcoxon", use_raw=True)
 
labels = [str(c) for c in adata.obs["cluster"].cat.categories]
result = {
    "method": "wilcoxon rank-sum, each cluster vs rest, log-normalised expression",
    "cluster_labels": labels,
    "markers": {},
}
 
for g in labels:
    df = sc.get.rank_genes_groups_df(adata, group=g)
    # ---- YOUR TURN: the table is sorted by score. Is that enough?
    #      Filter out genes with a small effect, e.g. df = df[df["logfoldchanges"] > 0.5],
    #      and think about which threshold is defensible.
    df = df.head(TOP_N)
    result["markers"][g] = [
        {"gene": r.names, "score": float(r.scores),
         "logfc": float(r.logfoldchanges), "pval_adj": float(r.pvals_adj)}
        for r in df.itertuples()
    ]
 
with open("out/markers.json", "w") as f:
    json.dump(result, f, indent=2)
 
# Print the top 5 per cluster to read them
for g in labels:
    print(f"cluster {g}:", ", ".join(m["gene"] for m in result["markers"][g][:5]))
 
record("marker_genes", method="wilcoxon", groupby="cluster", reference="rest", top_n=TOP_N)