---
title: "Graphics Dump"
date: 2022-11-15
draft: true
tags:
- Vulkan
- Linux
- Graphics Dump
---

This is a huge topic just by itself, but it's incredibly interesting as everything we said before is assuming that you're
either running your Vulkan program without any graphics output (_specifically_ presentation, as you can totally run the graphics
part of Vulkan headless).

For _brevity’s_ sake, and because there's already a lot of X11 information out there - I want to cover what specifically
happens on **Wayland**. This is especially troubling because there is a lot of misinformation on the web, especially around Wayland.

### On the Vulkan Side

Let's momentarily mention what exactly you need to do on Vulkan to get presentation working. We'll keep this short, but
it's important to get our bearings straight.

This may be a surprise to some, but Vulkan has nothing to do with presentation. This is pretty on par with Khronos APIs
actually, as OpenGL also did not concern itself with presentation (GLX, EGL, and other similar stuff is _not_ related).

In Vulkan, to get presentation you must enable a device extension, specifically `VK_KHR_swapchain`. This is not the only
piece of the puzzle, as you also need a surface to render to. There is a lot of options, but we are only concerning ourselves with two:

* `VK_KHR_surface` - this is the base surface extension
* `VK_KHR_wayland_surface` - needed to interface with the wayland client
* `VK_KHR_directfb_surface` - we will get into this later, as it provides a way to display vulkan directly to the framebuffer.

### Wayland

We'll be exclusively talking about how Vulkan applications under Wayland function, specifically under two scenarios.
One will be through a typical desktop environment - in this case - KDE Plasma as well as a more barebones example, bare KMS.
For both cases I will be using SDL2 instead of interacting with the Wayland layer itself,
which will be the case for many games. This does not change much though, because unlike OpenGL - SDL2 does not really interact
or intercept Vulkan functionality, apart from creating a Vulkan surface.

I chose these two situations because one is your more typical desktop environment, where the compositor has to juggle many
windows vying for presentation. The bare KMS example is more relevant to something like a game system, and we can see if
anything is different here in terms how the swapchain and presentation is handled.

### How swap chains work (quickly)

So how do swap chains work (quickly?) For simplicity, we're talking about a typical MAILBOX swap chain.

Next image is requested by the application.
If the image is still valid, its handle is returned to the application. This is also known as the _backbuffer_.
While the application can hold onto this image, they can draw anything they wish into it.
Once the application has finished rendering, it "presents" (note: the application is usually not directly presenting it to the screen)

### How do swap chains work (in real life)

Okay this sounds all well and good, but how does this work in _real life_? On a typical desktop environment, we have 
many different windows, some of which misbehave or malfunction and don't return and present images in time with our
display. Some of them even present _faster_ than the display, so who is managing this?

Now in this case, I'll be covering how Wayland compositors handle this, specifically KWin. While the same might apply to X11 environments,
Wayland is the future and it's way, way simpler to explain. 

First we have to remember that KWin itself, _is_ a graphics application and it also follows the same rules as any other. Right now, KWin
is built on OpenGL technologies but uses GBM to present stuff to the screen. Now KWin in this example, is the Wayland _server_ and other
applications are Wayland _clients_. This includes XWayland, which is simply wrapping the Xorg server as a Wayland client.

1. Your Vulkan application wants a Wayland surface, and is running on KWin Wayland.
2. It uses 

### What is GBM??

GBM stands for _"generic buffer management"_ and is also part of the Mesa project. It's mostly used to initialize EGL on DRM KMS. This is
Also meaningless to most people, including me. When researching _what_ GBM is, it's infuriating that there's really no simple explanation
to what it enables.

Okay, let's go with an example. You want to implement a desktop compositor, where do you begin?

Here's some simple requirements:
1. You want to make sure you're booted into DRM KMS.

So let's display something to the screen, such as 

You may have heard how Nvidia fought against Mesa with it's GBM, with EGLStreams before eventually conceding and
implementing GBM - this is why. Since Wayland compositors need to initialize graphics through DRM KMS, it eventually needs to allocate
memory. It does this via calling the Mesa GBM, which then in turn calls the GPU specific stuff.

## Conclusion

I hope this article clears up any misconceptions about the Linux graphics stack, and I definitely learned a lot while researching
This. While this was a nice overview of the entire stack, it would be really helpful if we could apply in this in a practical fashion,
so that's what I'm going to cover in the next article!
