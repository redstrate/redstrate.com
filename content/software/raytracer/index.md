---
title: "Raytracer"
date: 2020-02-17
draft: false
source: "https://codeberg.org/redstrate/raytracer"
license: MIT
projtags:
- CPlusPlus
- 3D
layout: "project"
aliases:
- /projects/raytracer
summary: "CPU raytracer."
---

This is a CPU-based raytracer, and also my first! This features things such as:

![Screenshot of a raytraced Suzanne](output.webp)

* Naive multi-threading support based on tiles and utilizing C++ futures.
* Ability to load arbitrary OBJs and render them.
* Indirect light sampling.
* Shadows!!
* dear imgui interface for easily viewing the results.
