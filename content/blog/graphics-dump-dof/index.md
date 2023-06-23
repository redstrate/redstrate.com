---
title: "Graphics Dump: Bokeh depth of field"
date: 2023-05-27
draft: true
series:
- Graphics Dump
---

Today I implemented Bart Wronski's fantastic Bokeh depth of field effect.

# Pitfalls

Here's some of the pitfalls I ran into while implementing this:

## Make sure the bokeh image doesn't repeat, or else it will start bleeding on the edge of triangles.

## Make sure your aperture texture has a black background.
