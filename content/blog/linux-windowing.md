---
title: "Graphics Dump: Surfaces and Wayland"
date: 2022-11-15
draft: false
tags:
- Vulkan
- Linux
series:
- Graphics Dump
---

**Note (2025-01-01):** This has been sitting in my drafts since 2022, and I don't have any immediate plans to finish it. So I thought I might as well post it for my own reference.

This is a huge topic just by itself, but it's incredibly interesting as everything we said before is assuming that you're
either running your Vulkan program without any graphics output (_specifically_ presentation, as you can totally run the graphics
part of Vulkan headless.) For _brevity’s_ sake, and because there's already a lot of X11 information out there - I want to cover what specifically
happens on Wayland.

# On the Vulkan Side

Let's momentarily mention what exactly you need to do on Vulkan to get presentation working. We'll keep this short, but
it's important to get our bearings straight. This may be a surprise to some, but Vulkan has nothing to do with presentation. This is pretty on par with Khronos APIs
actually, as OpenGL also did not concern itself with presentation (GLX, EGL, and other similar stuff is _not_ related).

In Vulkan, to get presentation you must enable a device extension, specifically `VK_KHR_swapchain`. This is not the only
piece of the puzzle, as you also need a surface to render to. There is a lot of options, but we are only concerning ourselves with two:

* `VK_KHR_surface`: this is the base surface extension
* `VK_KHR_wayland_surface`: needed to interface with the Wayland client
* `VK_KHR_directfb_surface`: we will get into this later, as it provides a way to display vulkan directly to the framebuffer.

# How swap chains work (quickly)

So how do swap chains work (quickly?) For simplicity, we're talking about a typical MAILBOX swap chain.

Next image is requested by the application.
If the image is still valid, its handle is returned to the application. This is also known as the _backbuffer_.
While the application can hold onto this image, they can draw anything they wish into it.
Once the application has finished rendering, it "presents" - although the application isn't in charge of actually presenting it to the screen.

# How do swap chains work (in real life)

Okay this sounds all well and good, but how does this work in _real life_? On a typical desktop environment, we have 
many different windows, some of which misbehave or malfunction and don't return and present images in time with our
display. Some of them even present _faster_ than the display, so who is managing this?

First we have to remember that KWin is a graphics application, and it also follows the same rules as any other. Right now, KWin
is built on OpenGL technologies but uses GBM to present stuff to the screen. Now KWin in this example, is the Wayland _server_ and other
applications are Wayland _clients_. This includes XWayland, which is simply wrapping the Xorg server as a Wayland client.

# What is GBM?

GBM stands for _"generic buffer management"_ and is also part of the Mesa project. It's mostly used to initialize EGL on DRM KMS. This is
Also meaningless to most people, including me. When researching _what_ GBM is, it's infuriating that there's really no simple explanation
to what it enables.

You may have heard how Nvidia fought against Mesa with it's GBM, with EGLStreams before eventually conceding and
implementing GBM - this is why. Since Wayland compositors need to initialize graphics through DRM KMS, it eventually needs to allocate
memory. It does this via calling the Mesa GBM, which then in turn calls the GPU specific stuff.

