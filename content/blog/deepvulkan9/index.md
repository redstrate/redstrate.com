---
title: "Vulkan Deep Dive: Parallax-corrected Reflections and Real-time Image-based Lighting"
date: 2022-10-05
draft: true
tags:
- Vulkan
- C++
- Deep Dive
---

You might be wondering why I'm covering reflections and IBLs in this series, as there
is tutorials covering these already online. However, there is two important distinctions in what I'm
teaching here:

_Parallax-corrected_ reflections and _Real-time_ Image-based Lighting. In most tutorials, they might cover
simple screen space reflections, or if you're lucky - cubemap-based solutions. Most image-based lighting tutorials also
limit themselves to existing HDRIs for simplicty, but doing it in real-time or offline when building levels
is arguably the more popular option in games, so it's harder to figure out that yourself. As always, let's dig in!

Although I'm covering two topics this time, I did it because they're tangentially related, but I won't be compromising on
the details.

## Parallax-corrected Reflections

This is something I've been wanting to cover for a long time, because despite still being popular in games, there is very
little information out there on how to accomplish this. For clarity, this is an extension of cubemap-based realtime (or offline) reflections
using some kind of probe globally or locally. The main difference is for regular reflections, there is no concept of it occupying
any real physical space, it's free-standing and doesn't look correct. For really rough or small reflections, it works okay but
look at how it looks in a watery environment:

And now with parallax-corrected:

As you can see, it's very convincing at most angles, and doesn't suffer from the downsides of screen-space reflections.

### Theory

### Implementation

## Real-time Image-based Lighting

This tutorial assumes that you _already_ implemented image-based lighting in your engine, as I won't dig into that here
(There is much smarter people to tell you how to do that!) This will just cover how to move from existing HDRI to one that is scene-based.

### Theory

_Note:_ This isn't really anything to do with any mathematical theory, but it's still a good subsection title ;-)

### Implementation