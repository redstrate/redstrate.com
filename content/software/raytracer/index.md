---
title: "Raytracer"
date: 2020-02-17T22:29:22-05:00
draft: false
source: "https://git.sr.ht/~redstrate/raytracer"
license: MIT
tags:
- C++
- 3D
resources:
- src: img/output.png
  name: Screenshot
layout: "project"
---

CPU raytracer.

<!--more-->
---

This is a CPU-based raytracer, and also my first! This features things such as:

* Naive multi-threading support based on tiles and utilizing C++ futures.
* Ability to load arbitrary OBJs and render them.
* Indirect light sampling.
* Shadows!!
* dear imgui interface for easily viewing the results.