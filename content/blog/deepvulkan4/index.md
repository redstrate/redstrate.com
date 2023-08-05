---
title: "Vulkan Deep Dive: CPU & GPU Culling"
date: 2022-10-05
draft: true
tags:
- Vulkan
- CPlusPlus
- Deep Dive
---

Culling is an important part of modern graphics, you definitely don't want anything you aren't looking at wasting
valuable resources.
<!--more-->
Now wait... what's the purpose of doing it ourselves? I think I read somewhere that GPUs will cull
objects itself, and won't try to rasterize them...

## Theory

So let's go over that naive approach, and how it doesn't work. Let's take this scene
with a lot of McGuire models, which if you don't know are stupidly high poly so thse are perfect for testing.

If you remember, GPUs will check if your triangles are even in the viewport, and will
dynamically cull them and prevent them from rasterizing - right?

## Implementation
