---
title: "Deep Dive: Linux Graphics Stack"
date: 2022-10-05
draft: true
tags:
- Vulkan
- Linux
- Deep Dive
---

The Linux graphics stack is a complex mechanism of many, many projects that function together to
deliver images to your screen. Since other operating systems hide this away from you, we fortunately have Linux to look
at for how a desktop system might deliver graphics.

You probably noticed this already, but this is a very long article. The idea is to give you a true "vertical slice" of a
typical Vulkan application. Other articles and videos may cover one or two subjects, but I go into excruciating detail
and want to give you the nitty gitty, especially for those who don't know what a "Mesa" is.

## Calling Vulkan

Let's begin by making a very simple Vulkan program, say - drawing a triangle. This is good because it covers a lot of
interesting stuff, picking a device to draw with, creating pipelines, render passes and issuing a draw call. I specifically
picked Vulkan for this article _because_ it makes swapchain management explicit which will be covered later.

So the first thing that should be noted is that under most circumstances, the first system in line when you call a Vulkan function
is actually not related to Linux graphics at all. It is called the Vulkan Loader.

_Note:_ This is true in most cases, but in some systems (say, a Nintendo Switch) you might link directly to the driver's Vulkan library.

The Vulkan Loader has a few jobs, but the one that is relevant to us is that handles ICDs. An ICD is an "Installable Client Driver",
because Vulkan is not specific to one vendor - and one system may have devices from multiple vendors (say, an integrated Intel
chipset and a dedicated AMD or Nvidia GPU), the Vulkan loader must send the right function calls to the right ICDs. The loader
also has a couple of more important jobs such as handling layers, but that is Vulkan-specific and will not be covered.

The Vulkan loader is usually called `libvulkan.so`, but let's dig a little deeper and find out what the ICD says. You may
find your installed ICDs in `/usr/share/vulkan/icd.d`. For example, here is the `radeon_icd.x86_64.json` found on the Steam Deck:
```json
{
  "ICD": {
    "api_version": "1.3.211",
    "library_path": "/usr/lib/libvulkan_radeon.so"
  },
  "file_format_version": "1.0.0"
}
```

_Note:_ It should be noted that 32-bit Vulkan drivers do exist, and the Vulkan loader handles switching to those as well. For example,
the Steam Deck also ships with an `radeon_icd.i686.json` file as well.

As you can see, the ICD format is incredibly simple, but the library we're interested in now is `/usr/lib/libvulkan_radeon.so`.

If we run `objdump` on this, we can get a complete list of functions from this:

```shell
$ objdump -T --demangle /usr/lib/libvulkan_radeon.so
...
```

As you can see, there is a **lot** of functions here - many more than I expected personally. If you notice, there is an interesting
pattern with the function signatures, they follow this:

* `wsi` - window screen interface
* `radv` - radeon, device-specific functions (for Vulkan device extensions)
* `vk_common` - for common vulkan functions that are not device specific, like `vkFlushMemoryRanges`
* Some game-specific names, such as `metro_exodus`. We'll come back to those.

Seeing this makes you think, "wait a second, what are some instance-level functions doing there?" Let's explain:

1. You call a Vulkan function, say - `vkCreateInstance`.
2. The Vulkan loader is actually what gets called, and it sends your call down the chain (through any layers, if needed) and eventually to the ICD.
3. The ICD then does what it needs to do (See: https://github.com/Mesa3D/mesa/blob/main/src/vulkan/runtime/vk_instance.c#L44)
4. Whatever that is returned is passed up

But, I chose `vkCreateInstance` for a very good reason. This happens _way_ before you even get to creating devices, so how
does it choose which driver to go with if it could be any of them? Well this is what is  called the "loader terminator", and it
specifically deals with this issue. TODO WRITE

Now let's move out of Vulkan and into Mesa, arguably the most important piece of the Linux graphics puzzle.

## Mesa

Mesa is the piece of software that is probably doing most of the heavy lifting here, and is an important piece of the
Linux graphics stack. Taken from their website:

```
Open source implementations of OpenGL, OpenGL ES, Vulkan, OpenCL, and more!
```

Oh... alright - well that doesn't really explain much. Let's look at their documentation which explains it better:

```shell
The Mesa project began as an open-source implementation of the OpenGL specification - a system for rendering interactive 3D graphics.

Over the years the project has grown to implement more graphics APIs, including OpenGL ES, OpenCL, OpenMAX, VDPAU, VA-API, XvMC, Vulkan and EGL.

A variety of device drivers allows the Mesa libraries to be used in many different environments ranging from software emulation to complete hardware acceleration for modern GPUs.

Mesa ties into several other open-source projects: the Direct Rendering Infrastructure, X.org, and Wayland to provide OpenGL support on Linux, FreeBSD, and other operating systems.
```

What's important to note that Mesa runs in _userspace_. As it says in the last line, it interfaces with kernel APIs such as
DRM (not to be confused with _digital rights management_, and don't worry the acronyms get more confusing).

Modern graphics drivers (and this applies to most desktop operating systems such as Windows and macOS) are split into two parts:
the kernel-space driver that interfaces directly with the hardware, and there is typically one per vendor, and then the userspace driver
that sits on top of the aforementioned layer and interacts with applications. The AMDGPU kernel driver is what we'll be covering today,
and the Mesa stack is our userspace driver. Specifically, we care about RADV.

### Mesa Drivers

Mesa comes with many drivers, which confusingly can be mixed and matched because they handle supporting different APIs.

* RADV is their AMD driver _for_ Vulkan. It has nothing to do with OpenGL support for this hardware (unless you use Zink ;-))
* ANV is their Intel driver _for_ Vulkan. As usual, it has nothing to do with OpenGL support for Intel chipsets.
* And so on...

Mesa not interfaces with the kernel DRI, which in turn calls a bunch of AMD-specific stuff
(in the case of RADV) in order to accomplish its goals. Again, this happens in _userspace_ as the kernel
driver only exists to facilitate I/O, load firmware and other really low level things.

So _what_ is DRI? Well, it's actually comprised of DRM and DRM KMS. So wait, how does this fit into OpenGL again? Well there's
another term, "Gallium".

### Gallium

This is so incredibly fascinating because for the longest time - whenever I think of "Gallium", I think
of "Gallium Nine" which is the way to run DX9 almost "natively" on your system via Mesa. But this has nothing to do with
that really, and is just another frontend to this system.

It's just a framework to reduce the amount of driver code needed to write OpenGL-compliant drivers. Unlike the
Vulkan device drivers, these drivers are located under `src/gallium/drivers`.

* radeonsi - RADV equivalent for OpenGL
* iris - Intel OpenGL support
* etc

### Overview 

So after going through all of that, I think we should take a step back and see what we have learned here.

1. You call `vkCreateInstance`
2. The Vulkan loader terminator eventually calls `vk_common_create_instance`, which exists in the Radeon ICD,
or the `/usr/lib/libvulkan_radeon.so` shared object. This object contains instance-level functions as well as device-specific
functions.
3. If the function is device-specific, the Mesa Vulkan driver knows how to interface with the driver
using the kernel APIs (DRI, which includes DRM KMS for modesetting and DRM for device interfacing).
4. The I/O leaves userspace (Mesa) and heads into the kernel (AMDGPU).
5. ...
6. The I/O returns to Mesa, and goes back up to the Vulkan Loader.
7. If needed (for example, enumerating all physical devices) the Vulkan loader terminator will combine the sources from multiple ICDs, otherwise
just leaves it alone.

Wow, that is a lot! And we learned with our brief OpenGL tangent that the process is very similar with Gallium. Now
of course this is nice and all, but what about WSI, swapchains and how those interact with Wayland?

Before we get into that, I would like to revisit the DRM subsystem in the kernel before we head back up to the userspace
portion.

## DRM

To remind us, DRM stands for the "Device Rendering Manager" and handles device-specific graphics guff. For us, the part
that's important is that it exposes device-specific APIs to control them from userspace. To find it in the kernel tree, see
`drivers/gpu/drm`.

Since we are just worrying about AMD gpus, you can see the AMD-specific bits in `drivers/gpu/drm/amd/amdgpu`. Inside
you'll see a metric ton of source and header files related to the amdgpu drm interface. Sweet!

Now I'm curious about how does Mesa then interface with these device-specific stuff? Does it just include the relevant kernel header? Let's find out...

If we take a look at the Mesa RADV `meson.build` we get our answer:

`dependencies : [ ..., dep_libdrm_amdgpu, ... ]`

Jackpot! This `dep_libdrm_amdgpu` bit is specifically referring to the libdrm project under the Mesa umbrella (https://gitlab.freedesktop.org/mesa/drm)
To get more confusing, this is _not_ DRM (the Linux subsystem) but rather a library sitting on top of it. Yes, really. To get even more
confusing, freedesktop.org also calls this library DRI for some reason. I told you the acronyms were going to get awful.

So, the Mesa RADV driver doesn't interface with the kernel directly, but rather access all the AMD-related
gubbins _through_ libdrm.

I won't be covering how the AMDGPU kernel driver actually works, partially because I don't know but the main idea is that
it basically operates on top of some proprietary firmware that's loaded on startup for the GPU. The DRM kernel driver is basically
responsible for creating a suitable interface, initializing firmware, memory and doing I/O between that and the userspace.

## Windowing

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
or intecept Vulkan functionality, apart from creating a Vulkan surface.

I chose these two situations because one is your more typical desktop environment, where the compositor has to juggle many
windows vying for presentation. The bare KMS example is more relevant to something like a game system, and we can see if
anything is different here in terms how the swapchain and presentation is handled.

### GBM

GBM stands for _"generic buffer management"_ and is also part of the Mesa project. It's mostly used to initialize EGL on DRM KMS. 

You may have heard how Nvidia fought against Mesa with it's GBM, with EGLStreams before eventually conceding and
implementing GBM - this is why. Since Wayland compositors need to initialize graphics through DRM KMS, it eventually needs to allocate
memory. It does this via calling the Mesa GBM, which then in turn calls the GPU specific stuff.