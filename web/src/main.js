import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { projectByHand } from './experiments.js';   // put this at the TOP of main.js
import { loadManifest, loadF32, loadU8, loadJSON } from './data.js';
import vertexShader from './shaders/points.vert.glsl?raw';
import fragmentShader from './shaders/points.frag.glsl?raw'; 

// ---- renderer, scene, camera ----
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('app').appendChild(renderer.domElement);
 
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x101114);
 
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.01, 100);
camera.position.set(0, 0, 3);
 
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
 
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
 
// Handy for the browser console (F12): type  cs.camera  etc.
window.cs = { THREE, renderer, scene, camera, controls };
 
window.cs.projectByHand = projectByHand;

// ---- CONTENT START ----

// ---- palette: sRGB values 0..1 straight into the shader (12 entries, see the vertex shader) ----
const hex = (h) => new THREE.Vector3(((h >> 16) & 255) / 255, ((h >> 8) & 255) / 255, (h & 255) / 255);
const PALETTE = [0x4e79a7, 0xf28e2b, 0xe15759, 0x76b7b2, 0x59a14f, 0xedc948,
                 0xb07aa1, 0xff9da7, 0x9c755f, 0xbab0ac, 0x1b9e77, 0x7570b3].map(hex);
// TODO (Part 3 will make you replace this by a colour-blind-safe palette)
 
const uniforms = {
  uWorldSize: { value: 0.03 },
  uPxPerUnit: { value: 1.0 },
  uHighlight: { value: -1.0 },
  uPalette:   { value: PALETTE },
};
 
function updatePointScale() {
  const h = renderer.getDrawingBufferSize(new THREE.Vector2()).y;       // pixels, incl. pixel ratio
  uniforms.uPxPerUnit.value = h / (2 * Math.tan(THREE.MathUtils.degToRad(camera.fov) / 2));
}
window.addEventListener('resize', updatePointScale);
updatePointScale();
 
let points = null, material = null, manifest = null, clusterCodes = null, markers = null;
 
function frameSphere(sphere, margin = 1.2) {
  const vFov = THREE.MathUtils.degToRad(camera.fov);
  const hFov = 2 * Math.atan(Math.tan(vFov / 2) * camera.aspect);
  const fov = Math.min(vFov, hFov);               // the tighter of the two
  const dist = (sphere.radius / Math.sin(fov / 2)) * margin;

  controls.target.copy(sphere.center);
  camera.position.copy(sphere.center).add(new THREE.Vector3(0, 0, dist));
  camera.near = dist / 100;
  camera.far = dist * 100;
  camera.updateProjectionMatrix();
  controls.update();
}

async function loadCells() {
  manifest = await loadManifest();
  const positions = await loadF32('/data/' + manifest.embeddings.pca.file);
  clusterCodes = await loadU8('/data/' + manifest.obs.cluster.file);
  markers = await loadJSON('/data/' + manifest.markers);
 
  if (positions.length !== manifest.n_cells * 3) throw new Error('positions: size mismatch');
  if (clusterCodes.length !== manifest.n_cells) throw new Error('cluster codes: size mismatch');
 
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('aCluster', new THREE.BufferAttribute(clusterCodes, 1));   // Uint8 -> float in the shader
 
  material = new THREE.ShaderMaterial({ uniforms, vertexShader, fragmentShader });
  points = new THREE.Points(geometry, material);
  scene.add(points);
  window.cs.points = points;
  hudInfo = `${manifest.n_cells} cells · PCA · ${manifest.obs.cluster.categories.length} clusters`;

  geometry.computeBoundingSphere();
  frameSphere(geometry.boundingSphere);
}
 
loadCells().catch((err) => { console.error(err); hud.textContent = String(err); });
function update(dt) { /* nothing to animate yet */ }
// ---- CONTENT END ----
 
// ---- HUD and render loop ----
const hud = document.getElementById('hud');
let hudInfo = '';
let frames = 0, last = performance.now(), prev = last;
 
function animate(now) {
  requestAnimationFrame(animate);
  update((now - prev) / 1000);
  prev = now;
  controls.update();
  renderer.render(scene, camera);
 
  frames++;
  if (now - last > 500) {
    hud.textContent = `${hudInfo}  ${Math.round(frames * 1000 / (now - last))} FPS`;
    frames = 0; last = now;
  }
}
requestAnimationFrame(animate);