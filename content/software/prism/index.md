---
title: "Prism"
date: 2020-08-11T22:29:22-05:00
draft: false
source: "https://git.sr.ht/~redstrate/prism"
license: MIT
tags:
- Prism
- 3D
- C++
- Vulkan
- Metal
resources:
- src: img/buddha.png
  name: Buddha Statue
- src: img/custom models.png
  name: Custom Models with Sphere
- src: img/pcss.png
  name: PCSS in action
- src: img/sponza.png
  name: Sponza example scene
featured: yes
layout: "project"
---

Cross-platform game engine specializing in the real-time rendering of physically-based graphics.

<!--more-->
---

{{< resource page="projects/prism" name="PCSS in action" >}}

This engine is the summation of all of my graphics developer knowledge. The list of features is not limited to:

* Physically based rendering and image based lighting based on scene probes or from a dynamic sky.
* Skeleton and also a basic cutscene system.
* Custom editors to edit the most common assets, such as materials and maps.
* Beautiful shadows using a runtime configurable option of PCSS, PCF or just plainly sampled.
* Scalability options including turning off all image based lighting or toning down point light shadowing which can run on lower end devices such as a phone.
* Advanced render interface layer that can run on top of Vulkan, Metal and eventually DirectX.
