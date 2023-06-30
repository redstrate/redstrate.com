---
title: "Graphics Dump: Drawing debug cubes"
date: 2023-06-28
draft: true
summary: "When working on my engine, I wanted to clean up my debug gizmos a bit. The first thing to tackle is drawing bounding boxes!"
tags:
- C++
- Math
series:
- Graphics Dump
---

When writing debug graphics, one of the most common shapes you might use are cubes. Usually to represent bounding boxes, but they're really versatile. I'll be showcasing a really simple technique you can implement to draw prettier debug boxes. Normally if you try to render a cube and only draw the wireframe, you end up with something like this:

"picture of a cube"

The diagonals are unnecessary here, and just add to the visual noise. That's something you typically want to avoid, especially in already packed debug screens. However, I found a pretty neat trick for removing these without having to change the vertex data. I just think it's a neat trick, even if it's a little odd. I don't remember if I made this up originally or found it somewhere else, some precursory searches didn't turn up much.

"cube positions"

You might be thinking of checking the vertex positions, comparing whether or not they're -1 or 1, and so on. But this won't work, or you'll end up with lopsided and complex logic. We can think
even simpler. Let's start by breaking it down just to one face, in two dimensions:

What is the _real_ difference between the outer edges and the diagonal? I'll give you a hint, it's not about the _position_ but the change in position.

Yes, it's that simple - we basically need to check if at least two components are not 0. In shader code, it will look something like this:

```glsl
bool is_x_okay = abs(inPosition.x) != 1.0;
bool is_y_okay = abs(inPosition.y) != 1.0;
bool is_z_okay = abs(inPosition.z) != 1.0;

int num_components = 0;
if (is_x_okay) {
    num_components += 1;
}
if (is_y_okay) {
    num_components += 1;
}
if(is_z_okay) {
    num_components += 1;
}

if (num_components < 2) {
    outColor = color;
} else {
    discard;
}
```

However this looks bad, we can definitely write this better. We have functions like notEqual, abs, and length to do component-wise comparisons.z
