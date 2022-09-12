---
title: "Resume"
---

https://redstrate.com | josh@redstrate.com

Self-committed and experienced programmer that can use multiple languages, various tools and self-taught experience to accomplish tasks ranging from low-level reverse engineering up to creating fully functioning game engines. Most proficient in systems programming languages such as C and C++.

Currently looking for an internship.

## Education

* AA from Florida State College of Jacksonville, 2018-2021.
* University of North Florida, since 2021 - expected to graduate in 2023.

## Technical Skills

To be written :-)

## Portfolio and Artifacts

More of my projects are accessible at https://redstrate.com/projects. Below is only a small selection.

### Prism: https://redstrate.com/projects/prism

Game engine which can render on top of the custom implemented RHI (Render Hardware Interface) which currently has Vulkan and Metal backends. The game engine also has several other subsystems, such as input handling, material compilation and asset pipelines. This engine differs from my previous ones as it is built with scalability in mind, and can even on lower end systems such as a phone. Some interesting effects are implemented that are typically found in most modern game engines, including physically based rendering, SMAA for anti-aliasing and PCSS for shadows.

### Silica Viewer: https://redstrate.com/projects/silica-viewer

Written to fill my own niche of viewing art canvases from a propietary art program that only runs on iOS devices called Procreate. Initial software was implemented using knowledge gleaned from other open source projects (credited in the repository) but quickly evolved into a much more complex application, involving replicating the original Procreate drawing engine including clipping layers, rendering masks and blending modes. An existing PSD writing library (called PSDWriter) was modified in order to support the more complex feature set I needed. The app is also currently published on the macOS App Store.

### Trinity: https://redstrate.com/projects/trinity

Also written to fill a niche of a nice looking Matrix client that copied Discord's interface. Does not use any pre-existing Matrix library, and was written solely on the Matrix specification. Originally written in 2018, but I revived it in 2022 by implementing some basic end-to-end encryption support which involved using libolm - a cryptography library.