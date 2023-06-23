---
title: "Graphics Dump: Drawing debug cubes"
date: 2023-06-27
draft: true
summary: "When working on my engine, I wanted to clean up my debug gizmos a bit. The first thing to tackle is drawing bounding boxes!"
tags:
- C++
- Graphics Dump
- Math
series:
- Graphics Dump
---

If you are writing graphical tools, one of the most common shapes you draw is boxes. They can represent areas (like the affected area of an environment capture) or a box collision.

One common problem that I run into, is dealing with these diagonals:

I found a pretty neat trick for removing these diagonals without having to change the vertex data. This doesn't work for anything that isn't a cube (I think), but whatever.

