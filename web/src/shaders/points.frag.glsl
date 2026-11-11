varying vec3 vColor;
 
void main() {
  vec2 p = gl_PointCoord * 2.0 - 1.0;      // -1..1 inside the point's square
  float r2 = dot(p, p);
  if (r2 > 1.0) discard;                   // cut the square to a disc
  gl_FragColor = vec4(vColor, 1.0);
 
  // TODO: soft edge, thin outline, or a fake sphere shading using p (see tasks)
}