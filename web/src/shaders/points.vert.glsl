attribute float aCluster;        // cluster code of this cell (0, 1, 2 ...)
uniform float uWorldSize;        // point diameter in world units
uniform float uPxPerUnit;        // H / (2 tan(fov/2)), set from JavaScript
uniform float uHighlight;        // cluster code to highlight, -1 for none
uniform vec3 uPalette[12];       // one sRGB colour per cluster code
 
varying vec3 vColor;
 
void main() {
  vec4 mv = modelViewMatrix * vec4(position, 1.0);   // model space -> view space
  gl_Position = projectionMatrix * mv;               // view space -> clip space
 
  gl_PointSize = uWorldSize * uPxPerUnit / -mv.z;    // pixels; -mv.z is the depth in front of the camera
 
  int code = min(int(aCluster + 0.5), 11);           // guard against an index outside the palette
  vColor = uPalette[code];
 
  // TODO (Part B tasks): use uHighlight to make the cells of one cluster larger and brighter
}