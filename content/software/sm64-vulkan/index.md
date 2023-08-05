---
title: "SM64-Vulkan"
date: 2022-10-03
draft: false
layout: "project"
projtags:
- SM64
- N64
- C
- CPlusPlus
license: Unknown
source: https://git.sr.ht/~redstrate/sm64
summary: "Fork of sm64-port for Linux using Vulkan."
---

This is my personal fork of [sm64-port](https://github.com/sm64-port/sm64-port). Why? Because it's fun! I'm simply
building on the great work already done by other people.

![Older WIP screenshot without blending support](13090-477b1a5c-8d3e-45e8-a77a-36e866a0c7b0.webp)

## Differences from sm64-port

Since I'm primarily a Linux user, I'm prioritizing Linux usage above everything else. I have already fixed a bunch of
Linux-specific bugs that I encountered (vsync timer issues, pulseaudio sync issues, and more). Stuff that does not
relate to this goal is bound to be removed or unmaintained (Windows support, native N64 support, etc.), and there are
better forks if you're looking for support of that stuff.

Oh yeah, I'm also building a Vulkan backend for the N64 renderer :-) By default OpenGL is used, but you can force Vulkan
by passing `-vulkan` when running the game.
