export async function loadJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Could not load ${url} (HTTP ${res.status})`);
  return res.json();
}
 
export const loadManifest = () => loadJSON('/data/manifest.json');
 
async function loadBuffer(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Could not load ${url} (HTTP ${res.status})`);
  return res.arrayBuffer();
}
 
export async function loadF32(url) { return new Float32Array(await loadBuffer(url)); }
export async function loadU8(url)  { return new Uint8Array(await loadBuffer(url)); }