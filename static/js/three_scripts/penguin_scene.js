function penguin_scene(sizeX, sizeY, container_id, resize_window) {
  var container, scene, camera, renderer, group;

  var targetRotationY = 0;
  var targetRotationYOnMouseDown = 0;
  var targetRotationZ = 0;
  var targetRotationZOnMouseDown = 0;

  var mouseX = 0;
  var mouseXOnMouseDown = 0;
  var mouseY = 0;
  var mouseYOnMouseDown = 0;

  var windowHalfX = sizeX / 2;
  var windowHalfY = sizeY / 2;

  init();
  animate();

  function init() {
    container = document.querySelector('#'+container_id);

    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(50, sizeX / sizeY, 1, 1000);
    camera.position.z = 50;
    scene.add(camera);

    var light = new THREE.AmbientLight(0xffffff, .8);
    camera.add(light);
    var light = new THREE.DirectionalLight(0xffffff, .2);
    camera.add(light);

    group = new THREE.Group();
    scene.add(group);

    // materials
    var blackMaterial = new THREE.MeshLambertMaterial({color: 0x000000});
    var whiteMaterial = new THREE.MeshLambertMaterial({color: 0xffffff});
    var orangeMaterial = new THREE.MeshLambertMaterial({color: 0xec9706});

    // body
    var backbody = new THREE.SphereGeometry(4.4,20,20,3,3.5,0,6);
    var mesh = new THREE.Mesh(backbody, blackMaterial);
    mesh.position.y = -5.25;
    group.add(mesh);
    var frontbody = new THREE.SphereGeometry(4.4,20,20,0.21,2.8,5,5);
    var mesh = new THREE.Mesh(frontbody, whiteMaterial);
    mesh.position.y = -5.25;
    group.add(mesh);
    
    // head
    var head = new THREE.SphereGeometry(3.75,20,20);
    THREE.ImageUtils.crossOrigin = true;
    var texture = new THREE.TextureLoader().load("http://i.imgur.com/xHQIAAI.png");
    texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
    texture.repeat.set( 1, 1 );
    var material = new THREE.MeshLambertMaterial( {color: 0xffffff, map: texture} );
    mesh = new THREE.Mesh( head, material );
    mesh.position.y = 1.75;
    group.add( mesh );

    // feet
    var leftfoot = new THREE.BoxGeometry(2,1,5);
    var mesh = new THREE.Mesh(leftfoot, orangeMaterial);
    mesh.position.y = -9.5;
    mesh.position.x = -1.5
    mesh.position.z = 2
    group.add(mesh);
    var rightfoot = new THREE.BoxGeometry(2,1,5);
    var mesh = new THREE.Mesh(rightfoot, orangeMaterial);
    mesh.position.y = -9.5;
    mesh.position.x = 1.5
    mesh.position.z = 2
    group.add(mesh);

    // arms
    var upperleftarm = new THREE.BoxGeometry(1,6,2);
    var mesh = new THREE.Mesh(upperleftarm, blackMaterial);
    mesh.position.y = -1;
    mesh.position.x = -5;
    mesh.position.z = 0.5;
    mesh.rotation.z = 1
    group.add(mesh);
    var lowerleftarm = new THREE.BoxGeometry(0.1,6,2);
    var mesh = new THREE.Mesh(lowerleftarm, whiteMaterial);
    mesh.position.y = -1.44;
    mesh.position.x = -5.3;
    mesh.position.z = 0.5;
    mesh.rotation.z = 1
    group.add(mesh);

    var upperrightarm = new THREE.BoxGeometry(1,6,2);
    var mesh = new THREE.Mesh(upperrightarm, blackMaterial);
    mesh.position.y = -1;
    mesh.position.x = 5;
    mesh.position.z = 0.5;
    mesh.rotation.z = -1
    group.add(mesh);
    var lowerrightarm = new THREE.BoxGeometry(0.1,6,2);
    var mesh = new THREE.Mesh(lowerrightarm, whiteMaterial);
    mesh.position.y = -1.44;
    mesh.position.x = 5.3;
    mesh.position.z = 0.5;
    mesh.rotation.z = -1
    group.add(mesh);

    // eyes
    var eye = new THREE.SphereGeometry(.6,20,20);
    eye.applyMatrix4(new THREE.Matrix4().makeScale(.75,1,1));
    var mesh = new THREE.Mesh(eye, blackMaterial);
    mesh.position.set(2,1,3);
    group.add(mesh);
    var mesh = new THREE.Mesh(eye, blackMaterial);
    mesh.position.set(-2,1,3);
    group.add(mesh);

    // nose
    var nose = new THREE.SphereGeometry(.6,20,20);
    nose.applyMatrix4(new THREE.Matrix4().makeScale(1,.8,1));
    var mesh = new THREE.Mesh(nose, orangeMaterial);
    mesh.position.set(0,.25,3.25);
    group.add(mesh);

    // snow
    var snow = new THREE.SphereGeometry(.75,20,20);
    var mesh = new THREE.Mesh(snow, whiteMaterial);
    mesh.position.y = 9.25;
    group.add(mesh);
    var mesh = new THREE.Mesh(snow, whiteMaterial);
    mesh.position.set(6,7,0);
    group.add(mesh);
    var mesh = new THREE.Mesh(snow, whiteMaterial);
    mesh.position.set(-6,7,0);
    group.add(mesh);
    var mesh = new THREE.Mesh(snow, whiteMaterial);
    mesh.position.set(-7,-3,0);
    group.add(mesh);
    var mesh = new THREE.Mesh(snow, whiteMaterial);
    mesh.position.set(7,-3,0);
    group.add(mesh);
    var mesh = new THREE.Mesh(snow, whiteMaterial);
    mesh.position.set(-8,2.25,0);
    group.add(mesh);
    var mesh = new THREE.Mesh(snow, whiteMaterial);
    mesh.position.set(8,2.25,0);
    group.add(mesh);
    
    renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true
    });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(sizeX, sizeY);
    container.appendChild(renderer.domElement);

    // TODO: Fix touch events to only react when over item
    document.querySelector('#'+container_id).addEventListener('mousedown', onDocumentMouseDown, false);
    document.querySelector('#'+container_id).addEventListener('touchstart', onDocumentTouchStart, false);
    document.querySelector('#'+container_id).addEventListener('touchmove', onDocumentTouchMove, false);

    window.addEventListener('resize', onWindowResize, false);
  }

  function onDocumentMouseDown(event) {
    event.preventDefault();
    document.querySelector('#'+container_id).addEventListener('mousemove', onDocumentMouseMove, false);
    document.querySelector('#'+container_id).addEventListener('mouseup', onDocumentMouseUp, false);
    document.querySelector('#'+container_id).addEventListener('mouseout', onDocumentMouseOut, false);
    mouseXOnMouseDown = event.clientX - windowHalfX;
    mouseYOnMouseDown = event.clientY - windowHalfY;
    targetRotationYOnMouseDown = targetRotationY;
    targetRotationZOnMouseDown = targetRotationZ;
  }

  function onDocumentMouseMove(event) {
    targetRotationY = targetRotationYOnMouseDown + (event.clientX - windowHalfX - mouseXOnMouseDown) * 0.2;
    targetRotationZ = targetRotationZOnMouseDown - (event.clientY - windowHalfY - mouseYOnMouseDown) * 0.2;
  }

  function onDocumentMouseUp(event) {
    document.querySelector('#'+container_id).removeEventListener('mousemove', onDocumentMouseMove, false);
    document.querySelector('#'+container_id).removeEventListener('mouseup', onDocumentMouseUp, false);
    document.querySelector('#'+container_id).removeEventListener('mouseout', onDocumentMouseOut, false);
  }

  function onDocumentMouseOut(event) {
    document.querySelector('#'+container_id).removeEventListener('mousemove', onDocumentMouseMove, false);
    document.querySelector('#'+container_id).removeEventListener('mouseup', onDocumentMouseUp, false);
    document.querySelector('#'+container_id).removeEventListener('mouseout', onDocumentMouseOut, false);
  }

  function onDocumentTouchStart(event) {
    if (event.touches.length == 1) {
      event.preventDefault();
      mouseXOnMouseDown = event.touches[0].pageX - windowHalfX;
      mouseYOnMouseDown = event.touches[0].pageY - windowHalfY;
      targetRotationYOnMouseDown = targetRotationY
      targetRotationZOnMouseDown = targetRotationZ;
    }
  }

  function onDocumentTouchMove(event) {
    if (event.touches.length == 1) {
      event.preventDefault();
      targetRotationY = targetRotationYOnMouseDown + (event.touches[0].pageX - windowHalfX - mouseXOnMouseDown) * 0.02;
      targetRotationZ = targetRotationZOnMouseDown + (event.touches[0].pageY - windowHalfY - mouseYOnMouseDown) * 0.02;
    }
  }

  function onWindowResize() {
    if (resize_window) {
      windowHalfX = window.innerWidth / 2;
      windowHalfY = window.innerHeight / 2;
      camera.aspect = window.innerWidth / innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, innerHeight);
    }
  }

  function animate() {
    requestAnimationFrame(animate);
    render();
  }

  function render() {
    group.rotation.y += (targetRotationY - group.rotation.y) * 0.1;
    group.rotation.z += (targetRotationZ - group.rotation.z) * 0.1;
    renderer.render(scene, camera);
  }

  console.log(1)
}