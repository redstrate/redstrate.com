---
title: "Vulkan Portability Initiative: The Death of My GFX Abstractions?"
date: 2021-09-12
draft: false
tags:
- Prism
- Vulkan
- Metal
---

In under an hour, I was able to port my already existing Vulkan code from [Prism](/projects/prism)
to Metal using [MoltenVK](https://github.com/KhronosGroup/MoltenVK). Here's a screenshot (very exciting):

![Screenshot of Prism running on macOS over MoltenVK](/articles/img/prism-on-mac-vulkan.png)

To clarify, Prism running on macOS is nothing new. In fact, a large portion of the engine was
developed natively on macOS using Metal. Vulkan was actually added after the fact, and since I already had plenty of
Vulkan experience it was no trouble. I initially chose to use Metal natively (over MoltenVK at the time) because the tooling was still too new, and I wanted to learn Metal. However something big has come along since then, the rise of the [Vulkan Portability Initiative](https://www.vulkan.org/portability)!

![Vulkan Portability Logo](/articles/img/Vulkan-Portability.svg)

The biggest thing to come out of this is the introduction of _first class macOS support_. If you've used the Vulkan SDK before on macOS, you _must_ give this new version a try. The new Vulkan SDK has an installer that takes cares of everything for you. Even the **Vulkan Configurator works**! This gets you the _same exact experience_ like as if you were developing with Vulkan on Windows or Linux. Yes, even the _Vulkan CMake module works out of the box_, thank you to every developer who worked on this!

![Screenshot of Vulkan configurator running on macOS](/articles/img/vkconfig-mac.png)

What does this mean for Prism? .. Not much yet except that it's awesome that it works pretty much of the box. However for any future graphics endaveours for me **I unfortunately won't be supporting Metal anymore**, there just isn't a reason to. I learned as much Metal as I wanted, and the Metal backend fullfilled that purpose. However, there's still a purpose to abstracting GFX away in Prism, _to make way for DirectX support_ :-)

---

By the way, I would be interested to see if anyone develops a Vulkan Portable Subset -> WebGPU translation layer (maybe implementing it as a vulkan driver ala MoltenVK?) This would be amazing, but I have yet to find
anyone interested in doing this. I would be especially interested as I'm not interested in learning _yet another_ API with it's own quirks, and... WSL - ugh. ~~Insert XKCD comic reference here~~

---

**Edit:** It turns out that I already hit a few snags with MoltenVK (which have [already been solved](https://github.com/KhronosGroup/MoltenVK/pull/1539)) so the Metal backend is restored. My point still stands though, that the future for my enthusiast projects might be only Vulkan.
