varying vec3 inPosition;

void main() {
    if (length(vec3(notEqual(abs(inPosition), vec3(1.0)))) > 1.0) {
        discard;
    } else {
        gl_FragColor = vec4(0, 1, 0, 1);
    }
}
