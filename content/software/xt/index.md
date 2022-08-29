---
title: "XT"
date: 2016-01-25T22:29:22-05:00
draft: false
tags:
- OpenGL
- C++
- 3D
resources:
- src: img/IMG_0160 copy.png
  name: Screenshot
layout: "project"
---

My first OpenGL based game engine.

<!--more-->
---

This was one of my first custom game engines, and my first foray into using OpenGL for a serious project. Unfortunately, I have lost all of the source code, but the image below is what I was able to save from a dear imgui screenshot thread.

From what I remember, it had the following features:
* Custom editor using dear imgui 
  * the tabbing library was based off of XYZ's engine since the docking branch did not exist at the time.
  * The editor also had auto-generated previews as shown for models, textures, and materials.
* Skybox support using cubemapping, this was also used for lighting my "PBR shader" (hint: as you can tell in the screenshot, I didn't know how to gamma correct anything in 2016.)

This is succeeded by my first Vulkan game engine, [Graph]({{< ref graph >}}). 
