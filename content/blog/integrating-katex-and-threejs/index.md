---
title: "Integrating KaTeX and Three.js into Hugo"
date: 2023-07-04
draft: true
tags:
- GLSL
- WebGL
- Math
- Hugo
threejs: true
math: true
---

My [last blog post]({{< ref "drawing-simple-cubes" >}}) integrates three.js and KaTeX into the article itself, which was a first for me. I want to use these libraries in future posts, so I want it to be easy and reusable.

# Three.js

If you aren't familiar, [three.js](https://threejs.org/) is an easy to use WebGL framework/engine and does a lot of useful work out of the box. When you just want to display a mesh, or a primitive and slap some materials on it you can't really get anything better. However, it wasn't very straightforward to integrate it and I also want to use custom GLSL shaders that complicates things a bit.

I self-host my own JavaScript files, and the easiest way to grab a ready-to-use distribution of three.js is from the repository under the "build" directory. Three.js complains in the console that it's not supported, although I'm not familiar what's the better way. To enable three.js for a specific post, I enable it via a parameter in the frontmatter:

```yaml
---
title: "Integrating KaTeX and Three.js into Hugo"
threejs: true
---
```

And then in `single.html` (or the layout you're using for posts) I check for the parameter and insert the JavaScript:

```go
{{ if .Params.threejs }}
    {{ $threejs := resources.Get "js/three.js" }}
    {{ if hugo.IsProduction }}
        {{ $threejs = $threejs | minify | fingerprint | resources.PostProcess }}
    {{ end }}
    <script src="{{ $threejs.RelPermalink }}" integrity="{{ $threejs.Data.Integrity }}"></script>
{{ end }}
```

That's only half the battle, as we still need to set up the scene and the render loop. To do this, I put the JavaScript files in the page directory. Then using this shortcode I insert a three.js scene inline:

```go
{{ $path := .Get 0 }}
{{ $id := .Get 1 }}
<div class="threejs-canvas" id="{{ $id }}"></div>
<script type="module" src="{{ $path }}"></script>
```

This adds a container and the script itself, and can be used as so:

```
{ {< three-scene "scene.js" "scene" >} }
```
("scene.js" is of course the script path, and "scene" is the name of the container.)

On the three.js side, we query for the container and add the canvas to it:

```javascript
document.getElementById('scene').appendChild(renderer.domElement);
```

I add some CSS to the container to take up 50% of the article width, so we need some way to automatically tell three.js to resize as the canvas changes. First, add a ResizeObserver that calls a `resize()` function:

```javascript
const resizeObserver = new ResizeObserver(resize);
resizeObserver.observe(renderer.domElement, {box: 'content-box'});
```

The resize function is as follows, which is updating the renderer size and the camera aspect ratio:

```javascript
function resize() {
  const canvas = renderer.domElement;
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;

  // you must pass false here or three.js sadly fights the browser
  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}
```

Right now this has to be set up for each and every JavaScript file, but I should move it into a common file for all of them later down the road. If you want to

## KaTeX

[KaTeX](https://katex.org/) is a LaTeX-compatible JavaScript math renderer, and so much easier to integrate than three.js. There's three files we need to include, `katex.js`, `katex.css` and `auto-render.js` (from the `contrib` folder).

# Credits

* This [StackOverflow answer](https://stackoverflow.com/a/45046955) explaining how to inform three.js about canvas resizes.
* ["Math Typesetting in Hugo"](https://mertbakir.gitlab.io/hugo/math-typesetting-in-hugo/) for a guide on how to use KaTeX.
