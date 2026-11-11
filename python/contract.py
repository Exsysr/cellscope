import json, os, shutil
import numpy as np
 
OUT = "../web/public/data"          # all scripts run from inside python/
 
 
def _path(name):
    os.makedirs(OUT, exist_ok=True)
    return os.path.join(OUT, name)
 
 
def load_manifest():
    with open(_path("manifest.json")) as f:
        return json.load(f)
 
 
def save_manifest(manifest):
    with open(_path("manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
 
 
def write_f32(name, arr, n_cols=3):
    """Write an (N, n_cols) array as little-endian float32."""
    a = np.asarray(arr)
    assert a.ndim == 2 and a.shape[1] == n_cols, f"expected (N, {n_cols}), got {a.shape}"
    assert np.isfinite(a).all(), "NaN or infinity in data"
    np.ascontiguousarray(a, dtype="<f4").tofile(_path(name))
 
 
def write_u8(name, arr):
    """Write a 1D array of integers 0..255 as uint8."""
    a = np.asarray(arr)
    assert a.ndim == 1, f"expected 1D array, got {a.shape}"
    assert a.min() >= 0 and a.max() <= 255, "values outside 0..255 cannot be stored as uint8"
    np.ascontiguousarray(a, dtype=np.uint8).tofile(_path(name))
 
 
def sync_provenance():
    """Copy the current provenance log next to the data files."""
    shutil.copy("out/provenance.json", _path("provenance.json"))