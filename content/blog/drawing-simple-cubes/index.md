---
title: "Drawing simple cubes"
date: 2023-06-10
draft: true
summary: "When working on my engine, I wanted to clean up my debug gizmos a bit. The first thing to tackle is drawing bounding boxes!"
tags:
- C++
---

If you are writing graphical tools, one of the most common shapes you draw is boxes. They can represent areas (like the affected area of an environment capture) or a box collision.

One common problem that I run into, is dealing with these diagonals:

Of course this is natural due to the way that GPUs work, they work in triangles and when drawing the wireframe of a cube doesn't just draw the edges but everything in-between:



