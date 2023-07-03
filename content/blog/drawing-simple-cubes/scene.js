const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer();
//renderer.setSize( window.innerWidth, window.innerHeight );
document.getElementById('scene').appendChild( renderer.domElement );

const geometry = new THREE.BoxGeometry(2, 2, 2);
const material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
material.wireframe = true;
const cube = new THREE.Mesh( geometry, material );
scene.add(cube);

camera.position.z = 5;

function resizeCanvasToDisplaySize() {
  const canvas = renderer.domElement;
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;

  // you must pass false here or three.js sadly fights the browser
  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();

  // set render target sizes here
}

function animate() {
	requestAnimationFrame( animate );

	cube.rotation.x += 0.01;
	cube.rotation.y += 0.01;

	renderer.render(scene, camera);
}

animate();

const resizeObserver = new ResizeObserver(resizeCanvasToDisplaySize);
resizeObserver.observe(renderer.domElement, {box: 'content-box'});
