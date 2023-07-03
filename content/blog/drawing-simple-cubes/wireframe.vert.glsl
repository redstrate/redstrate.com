varying vec3 inPosition;

void main() {
    inPosition = position;

    gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}
