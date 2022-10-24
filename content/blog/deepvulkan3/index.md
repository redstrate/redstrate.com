---
title: "Vulkan Deep Dive: SMAA"
date: 2022-10-05
draft: true
tags:
- Vulkan
- C++
- Deep Dive
---

In this Vulkan deep dive, we'll go over a simple but important technique - anti-aliasing. FXAA is a popular
and cheap choice for a post-processing AA solution, but SMAA is another popular option used in many games. Not only is it
cheap (but not as cheap as FXAA), it's also extremely easy to implement. It has a HLSL and GLSL version, but of course
we're just worrying about a Vulkan implementation here.

## How SMAA Works

Compared to FXAA, SMAA requires extra post processing passes, let's go over all of them and their purpose.

## Implementation

### Getting Files

### Choosing Passes

### Setting up new Render Passes

### Testing

## Conclusion