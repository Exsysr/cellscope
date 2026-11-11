import * as THREE from 'three';

// Transform cell number i from model space to pixel coordinates, step by step.
export function projectByHand(i) {
  const { camera, points, renderer } = window.cs;
  const pos = points.geometry.attributes.position;
  const v = new THREE.Vector4(pos.getX(i), pos.getY(i), pos.getZ(i), 1);
  camera.updateMatrixWorld();
  points.updateMatrixWorld();
  console.log('model space:', v.toArray());

  // 1: world space
  v.applyMatrix4(points.matrixWorld);
  console.log('world space:', v.toArray());

  // 2: view (camera) space
  v.applyMatrix4(camera.matrixWorldInverse);
  console.log('view space:', v.toArray());

  // 3: clip space
  v.applyMatrix4(camera.projectionMatrix);
  console.log('clip space:', v.toArray());

  // 4: NDC (perspective divide)
  const ndc = new THREE.Vector3(v.x / v.w, v.y / v.w, v.z / v.w);
  console.log('NDC:', ndc.toArray());

  // 5: pixels (NDC [-1,1] -> canvas size, y is flipped)
  const canvas = renderer.domElement;
  const w = canvas.clientWidth;
  const h = canvas.clientHeight;
  const px = (ndc.x * 0.5 + 0.5) * w;
  const py = (1 - (ndc.y * 0.5 + 0.5)) * h;
  console.log('pixels:', [px, py]);

  // Reference result from the library for comparison:
  const ref = new THREE.Vector3(pos.getX(i), pos.getY(i), pos.getZ(i)).project(camera);
  console.log('library NDC:', ref);

  return { px, py, ndc };
}