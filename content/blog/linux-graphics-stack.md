---
title: "Graphics Dump: Mesa, Vulkan and DRM"
date: 2022-11-15
draft: false
tags:
- Vulkan
- Linux
- Graphics Dump
- KDE
comments:
  host: mastodon.art
  username: redstrate
  id: 109349980860736142
series:
- Graphics Dump
---

The Linux graphics stack is a complex mechanism of many projects that function in unison to deliver images to your screen. How do they work?

<!--more-->

_Graphics Dump_ is a new articles series I'm starting, geared towards tutorials and documentation for graphics-related things that are obscure but interesting. There are a thousand graphics tutorials covering how to start drawing in OpenGL, how to implement shadow mapping, and so on - but how many cover how stuff like how _Mesa_ works? I hope these fill someone's weird niche, like they do for me - so please enjoy!

{{<toc>}}

### Introduction

Since other operating systems hide these processes away from you, it is fortunate that Linux exists to easily showcase how typical desktop graphics systems function! Of course other systems like Windows, macOS, and other operating systems function differently - but a lot of the same concepts apply (API call dispatch, userspace graphics drivers, and display planes as some good examples.)

However, the scope of this article has ballooned tremendously, so I had to split it into multiple parts in order to get _something_ finished. Right now we'll cover a "vertical slice" or overview of the typical call stack of a Vulkan application, and later articles will deep dive into how we can wrangle GBM to display graphics, how VR headsets fit into this ecosystem, and more interesting topics that require a dedicated article.

This article is geared towards understanding the Linux graphics stack to graphics developers like me, who primarily work with graphics APIs and sort of is confused by Mesa, DRM and other such projects. As such, I kind of hand-waive over stuff like device creation, low-level GPU functions and other terms I expect you should know already or I'm not qualified to cover.

### Vulkan

I don't intend to talk much about Vulkan itself here, as this is an article dedicated to the graphics stack as a whole, not just one API. However I want to clarify some misconceptions about Vulkan first.

* Vulkan is a graphics and compute API. Without extensions, it has no way to interact with window surfaces, displays, and perform presentation among other things you might expect.
* Vulkan is standardized by Khronos, which are not the ones who typically implement Vulkan (which would be your graphics driver developers.)
* Although Vulkan is spearheaded by Khronos, there are a lot of companies that back, develop for, and contribute back to the ecosystem such as LunarG, Collabora, Intel, AMD, NVIDIA and even Nintendo[^1].

With that out of the way, let's talk about how Vulkan applications typically interact with your system:

#### Calling Vulkan

Let's say we have a very simple Vulkan program, all it does is open a window and draw a triangle. The reason why I chose Vulkan as the graphics API for this article is because it is so involved: you need to create a device, create shader pipelines, render passes and submit draw calls and perform explicit presentation sync. Vulkan's explicit swapchain management and synchronization makes it much easier to show what happens for the purpose of these articles. OpenGL and other API hide that information from you.

When we call something like `vkCreatePipeline` (a call that bundles some draw information with one or more shaders) the first library you will encounter is the _"Vulkan Loader"_, not any graphics driver. The Vulkan Loader is an independent project not related to Linux graphics at all.

#### Vulkan Loader

The Vulkan Loader does a lot more than wrap Vulkan calls, but the one that is relevant to us is that handling ICDs. "ICD" stands for _"Installable Client Driver"_, this is the actual graphics driver.

The reason ICDs even exist as a concept is hinted in the name: Vulkan is not specific to one vendor and sometimes you may have ICDs from multiple vendors (say, an integrated Intel chipset and a dedicated AMD/Nvidia GPU). You cannot simply link or refer to one specific vendor's implementation of Vulkan, because Vulkan is inherently cross-platform, cross-vendor and a big feature is it's portability[^2].

On Linux, the Vulkan Loader is installed as `libvulkan.so`, but let's dig a little deeper and find out what what ICD we're using. ICDs are typically installed in `/usr/share/vulkan/icd.d`. Here is the `radeon_icd.x86_64.json` found on the Steam Deck[^3]:

```json
{
  "ICD": {
    "api_version": "1.3.211",
    "library_path": "/usr/lib/libvulkan_radeon.so"
  },
  "file_format_version": "1.0.0"
}
```

ICDs are defined in plain JSON and we can find the driver library in `library_path`. We're focusing on AMD hardware in this article, but you can apply the same processes to Intel hardware and any other Mesa-supported driver.

#### Inside of an ICD

Let's start by running `objdump` on our driver, so we can get a complete list of functions:

```shell
$ objdump -T --demangle /usr/lib/libvulkan_radeon.so
...
```

If you run this on your system (and of course substitute the library if you're not on an AMD system), you'll see there is a **lot** of functions. If you're keen enough, there is a distinct pattern in function signatures:

* `wsi` - window screen interface related functions.
* `radv` - device-specific functions.
* `vk_common` - common vulkan functions that are not device specific, like `vkFlushMemoryRanges`. We'll get to why these are included here at all later.
* Weirdly enough, video game names such as `metro_exodus`. We'll come back to why those are even a thing in a future article.

Seeing this might make you think, _"wait a second, what are some instance-level functions doing there?"_ If you aren't familiar with Vulkan, it's functions have two distinct levels to them:

* Instance-level functions: `vkCreateInstance`, `vkEnumeratePhysicalDevices` and so on. These do not require a device to be used.
* Device-level functions: `vkCreateGraphicsPipelines`, `vkBeginCommands`. These do need a logical device to operate.

However, if you haven't noticed already - there is functionally no difference between these two levels: they are technically part of the same driver, **so how does the Vulkan loader know which driver to use**?

The answer is simple, it just calls all of them! When you call a Vulkan function through the Vulkan Loader system, if it's a device-level call it simply passes it down to the driver that the device belongs to - but if it's an instance-level function, it actually "aggregates" the data from the relevant drivers. This is what is called the "Loader Terminator".

#### How the Loader Terminator Works

A good example to showcase this is `vkEnumeratePhysicalDevices`, and as the name implies, gives you a list of the physical devices on the machine. If you have a Intel integrated GPU and say, a  NVIDIA GPU, this is what the loader terminator might do:

* Control is eventually handed down to the Vulkan Loader, from your call to `vkEnumeratePhysicalDevices`.
* The Loader realizes this is an instance-level function, and one that needs aggregate data from all devices.
* The Loader then calls your ICDs, which might be `libnvidia_vulkan.so` and `libintel_vulkan.so` (these aren't actual library names, I just made them up!)
* Once control is handed back to the Loader, it then combines the physical device lists from both devices and hands the data back to your application.

This is actually a really smart design, since it would be near-useless if `vkEnumeratePhysicalDevices` only listed devices from _one_ ICD. And then once you create the logical device from that ICD's physical device, the Loader takes care of figuring out which ICD you actually want to talk to without you even realizing it. The fact that I didn't even know what a "loader terminator" was or that it even did this in the first place is a testament to how nicely this system functions.

#### Overview

That was a _lot_ of information to parse, so let me give a quick overview of how Vulkan calls eventually each your graphics driver:

1. You call a device-specific function like `vkQueueSubmit`.
2. The Vulkan Loader picks up your call, determines the correct ICD from th device you passed to the function.
3. The graphics driver then does its job. (For example, here's [the implementation of vkCreateInstance](https://gitlab.freedesktop.org/mesa/mesa/-/tree/main/src/vulkan/runtime/vk_instance.c#L44). We'll get into why this is separated from the driver later.)
4. The function result is passed back up, through the call stack, to your application.

This is of course assuming there are no layers activated (which are simply other programs that can intercept Vulkan calls) which may change the route your call makes. Now let's take a look at what your graphics driver actually is, and it's more complex than you might think.

### Mesa

Mesa is the next piece of software in this call stack (the ICD). It does most of the heavy lifting here, and is an important piece of the Linux graphics stack. However, I've seen people confused on _what_ Mesa is - so let's take a look at their [website](https://mesa3d.org):

```
Open source implementations of OpenGL, OpenGL ES, Vulkan, OpenCL, and more!
```

Oh... alright - well that doesn't really explain much. Let's look at [their documentation](https://docs.mesa3d.org) which explains it better:

```
The Mesa project began as an open-source implementation of the OpenGL specification - a system for rendering interactive 3D graphics.

Over the years the project has grown to implement more graphics APIs, including OpenGL ES, OpenCL, OpenMAX, VDPAU, VA-API, XvMC, Vulkan and EGL.

A variety of device drivers allows the Mesa libraries to be used in many different environments ranging from software emulation to complete hardware acceleration for modern GPUs.

Mesa ties into several other open-source projects: the Direct Rendering Infrastructure, X.org, and Wayland to provide OpenGL support on Linux, FreeBSD, and other operating systems.
```

It's important to note that Mesa runs in _userspace_. As it says in that last sentence, it interfaces with kernel APIs such as
DRM (not to be confused with _digital rights management_, and don't worry the acronyms get more confusing) and a whole lot of other stuff. These other projects will also be covered in this article and in other future ones.

Linux graphics drivers are split into two parts:
the kernel-space module that interfaces directly with the hardware, and the userspace driver
that sits on top of that kernel layer and interacts with applications. Mesa implements that user space layer for us, for other vendors like NVIDIA and AMD's own proprietary solution have their own userspace layer[^4]. 

Let's take a look at how Mesa is structured, and how they can reuse code between many devices and drivers. This will also explain the curious structure of the `objdump` from earlier, and what the `radv` prefix is referring to.

#### Mesa Drivers

Mesa comes with many drivers, and each driver has a name (`radv`, `iris`, etc) which is unique even across  different APIs:

* RADV: the modern AMD driver _for_ Vulkan. It has nothing to do with OpenGL support.
* ANV: the modern Intel driver _for_ Vulkan.
* radeonsi: Modern AMD driver but for OpenGL!
* iris - Modern Intel OpenGL support
* And so on...

However Mesa has a _lot_ of drivers, and you might think it become unmaintainable - I mean supporting one graphics API is trouble enough, but Mesa somehow supports all of these drivers and all of these APIs? How do they accomplish such a feat?

#### Gallium

Let's take a look at how their OpenGL support works first, which is easier to explain. This is so incredibly fascinating because for the longest time - whenever I think of "Gallium", and other people
probably relate - I think of [Gallium Nine](https://docs.mesa3d.org/gallium-nine.html) which is the way to run DX9 almost natively on your system via Mesa. However, Gallium Nine is simply another frontend to Gallium.

Gallium is a framework to reduce the amount of driver code needed to write OpenGL-compliant drivers. These drivers are located under `src/gallium/drivers` in [the Mesa source code](https://gitlab.freedesktop.org/mesa/mesa/-/tree/main/src/gallium/drivers). OpenGL has a lot of state work and other boring stuff that typically doesn't vary from driver to driver, so this is lifted into the Gallium State Tracker and then the device drivers can focus more on what they're there to do, which is interface with the hardware. So when bringing up a new system that needs OpenGL support, you just need to write a Gallium driver which takes way, way less work than writing a new OpenGL driver from scratch.

However you might be wondering how Mesa structures it's installed OpenGL drivers. Mesa provides `libGL.so` which plays a similar role to `libvulkan.so`, and selects the correct OpenGL driver at runtime[^5].

#### Vulkan

Now unfortunately Mesa doesn't have a fancy name for its Vulkan driver framework (as far as I know!) because this is mostly a new development. Previously, a lot of Mesa's Vulkan drivers implemented a whole of duplicate Vulkan work (like in instance-level functions, but also a lot of queue-related things) which wasn't a huge deal, but now that Mesa has way more Vulkan drivers (they have RADV, ANV, and soon NVK - and that's not all of them!) the work was piling up and implementations started to drift apart. Apparently a lot of RADV and subsequent Vulkan drivers were based off of ANV, and then common Vulkan code got lifted outside of the drivers later. As Jason Ekstrand says in ["Introducing NVK"](https://www.collabora.com/news-and-blog/news-and-events/introducing-nvk.html):

> One of my personal goals for NVK is for it to become the new reference Vulkan driver within Mesa. All of the Vulkan drivers in Mesa can trace their lineage back to the Intel Vulkan driver (ANV) and were started by copying+pasting from it. We won't be there for a while, but my hope is that NVK will eventually become the driver that everyone copies and pastes from. To that end, I'm building NVK with all the best practices we've developed for Vulkan drivers over the last 7.5 years and trying to keep the code-base clean and well-organized.

As we've seen though, the RADV ICD simply contains _both_ the common Vulkan code and then the RADV specific stuff (prefixed with `radv`) and it's all inside of just one object library. The library is then aptly named `libvulkan_radeon.so`.

Now that we covered how Mesa separates and abstracts drivers for Vulkan and OpenGL, how do the device drivers actually function? Well depending on the structure of the hardware and its unique quirks, a lot of care has to go into optimizing the API the driver is handling. But how does it actually _interact_ with the hardware?

### DRI

The answer is not so simple. You may have heard terms like DRI, DRM, KMS, DRM KMS and other things but these aren't very well explained. Mesa uses something called DRI.

DRI stands for _"Direct Rendering Infrastructure"_ and is something specific to Linux. The DRI is an umbrella term also covering _DRM_ and _DRM KMS_. 

#### DRM

DRM stands for _"Direct Rendering Manager"_ and refers to the DRM system that exists in the kernel. This is what the AMDGPU kernel module implements, and consequently how Mesa is able to interface with the GPU at all. It basically creates an API for userspace applications to access your GPU. The kernel module handles facilitating I/O, loading firmware and other low level things. To find the in-tree DRM kernel modules, see `drivers/gpu/drm`.

Since we are just covering modern AMD GPUs, the AMDGPU module is located under `drivers/gpu/drm/amd/amdgpu`. Inside you'll see a metric ton of source and header files related to the amdgpu drm interface. Sweet!

Now you might be curious how does Mesa then interface with these device-specific stuff? Does it just include the relevant kernel header? But don't those break often? It would also be weird for Mesa to break between kernel versions too[^6].

If we take a look at [the meson.build for vulkan_radeon](https://gitlab.freedesktop.org/mesa/mesa/-/blob/main/src/amd/vulkan/meson.build#L177) we get our answer:

`dependencies : [ ..., dep_libdrm_amdgpu, ... ]`

Jackpot! What is this `libdrm` it mentions? It actually is specifically referring to the [libdrm project](https://gitlab.freedesktop.org/mesa/drm).

So, the Mesa drivers doesn't interface with the kernel directly, but rather access all the device-specific functionality _through_ libdrm. This is because kernel interfaces are not truly stable and the interface isn't really meant for application consumption anyway, libdrm handles all of that for Mesa. This is also might be why Mesa doesn't define a specific kernel requirement, because it technically doesn't depend on their DRM interface.

#### DRM KMS

The other major part of the DRI project is "DRM KMS", one part we now know is "Direct Rendering Manager" but what is "KMS"? It stands for "Kernel Mode Setting" and is used on modern Linux systems to initialize and configure the framebuffer. You might think that "DRM KMS" stands for a type of "KMS" but really it can't exist _without_ using DRM. You'll also sometimes see it written as "DRM/KMS" which is weird but I guess it's typical in the Linux world (like GNU/Linux.)

Modesetting refers to initializing the display, handling EDIDs and all of that fun stuff. "KMS" is then referring to doing this in the kernel instead of in user space. You might be thinking that meant that user space was initializing the GPU's connected screen and you'll be right, which was slow especially when switching to things like the TTY (which is handled by the kernel) since it had no idea what the user space was doing.

#### Quick Note about DRI versions

You may have noticed this already, but there are things called DRI1, DRI2, DRI3. There are actually three different versions of DRI, which has evolved as the needs of graphics drivers and desktop compositors changed. We're currently on DRI3 and that's what I'll be covering once we get into presentation and synchronization. 

### Conclusion

I hope this gives you a nice overview of what libraries are involved when dealing with Linux graphics, and an explanation of some of the terms you might have seen before. As stated in the beginning, this has grew and grew in scope so I'm cutting the article here so I can get it published first.

In the next part we'll be covering how windowing, synchronization and presentation works under KWin, a popular but also typical Wayland compositor. We'll also cover how GBM, DRI3 and KMS fit into the picture and why they were created in the first place. This will also include an example of wrangling GBM and Vulkan to display something to the screen and why `VK_KHR_display` isn't being used more.

I'm not a Mesa nor an AMD developer, so if you see any mistakes feel free to contact me! Otherwise please enjoy and make sure to check out these other fine webpages below.

### See Also

* [Mesa Documentation](https://docs.mesa3d.org/index.html)
* [Mesa Source Code](https://gitlab.freedesktop.org/mesa/mesa)
* ["Introducing NVK" on the Collabora blog](https://www.collabora.com/news-and-blog/news-and-events/introducing-nvk.html) - goes over some history of the Mesa Vulkan drivers and how NVK will eventually fit in.
* ["Architecture of the Vulkan Loader Interfaces"](https://github.com/KhronosGroup/Vulkan-Loader/blob/master/docs/LoaderInterfaceArchitecture.md) - Detailed explanation of how the Vulkan Loader functions, a good read if you're still interested in how Vulkan functions outside the scope of this series.
* [DRI on Wikipedia](https://en.wikipedia.org/wiki/Direct_Rendering_Infrastructure) - Really good overview of the DRI system on Wikipedia, actually all of the Linux articles are surprisingly good quality.
* ["The DRM/KMS subsystem from a newbie’s point of view"](https://events.static.linuxfound.org/sites/events/files/slides/brezillon-drm-kms.pdf) - Good overview of how DRM KMS functions and how compares to fbdev, but is geared towards how to use DRM as an API.
* [The Linux Graphics Stack series by Iago Toral](https://blogs.igalia.com/itoral/2014/07/29/a-brief-introduction-to-the-linux-graphics-stack/) - Really good series on the Linux graphics stack by an actual Mesa developer!

[^1]: See https://www.khronos.org/conformance/adopters/conformant-companies#vulkan for a list of companies that have implemented Vulkan. This is _not_ a list of companies that have pitched some sort of contribution back to Vulkan, but is also a good indicator that they employ individuals or companies that have or they also published Vulkan extensions on their behalf.

[^2]: While this is true on the desktop (where drivers are installable), Vulkan is equally suited for embedded purposes and game consoles. It's possible to link directly to your driver's Vulkan library if needed. When developing for the Nintendo Switch, the Vulkan Loader is an unnecessary maintenance burden where portability between drivers is a non-issue.

[^3]: While we're taking a look at a 64-bit Vulkan driver, 32-bit Vulkan drivers do exist (and needed for those 32-bit games that somehow still get made), and the Vulkan Loader handles switching to those as well. The Steam Deck ships with an `radeon_icd.i686.json`.

[^4]: I've seen a lot of confusion online as to the relation between Mesa, AMDGPU-Pro and NVIDIA. To be clear, Mesa _only_ implements the userspace drivers for OpenGL, Vulkan, OpenCL etc and AMDGPU-Pro, NVIDIA's proprietary solutions completely sidestep that. Curiously, AMDGPU-Pro reuses the existing AMDGPU kernel module used by Mesa's AMD drivers unlike NVIDIA which provides their own kernel modules (which were recently open-sourced). On a typical NVIDIA Linux system, Mesa is typically not touched and everything is routed through NVIDIA's software stack.

[^5]: See Iago Toral's ["Driver loading and querying in Mesa"](https://blogs.igalia.com/itoral/2014/09/04/driver-loading-and-querying-in-mesa/) for a good overview of how Mesa accomplishes this.

[^6]: Some versions of Mesa actually _do_ require specific kernel versions, however as far as I know this is an undocumented requirement. 

