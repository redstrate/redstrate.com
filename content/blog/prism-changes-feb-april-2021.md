---
title: "Prism Changelog: Feburary and April 2021"
date: 2021-04-04
draft: false
tags:
- Prism
aliases:
- /articles/prism-changes-feb-april-2021/
---

These two months contain some pretty big changes I made to Prism, following a short hiatus from the project. These include some pretty important changes to the project moving forward and I hope to keep documenting these in this nice and concise, visual way in the future! <!--more--> Also before you ask, this is Feburary _and_ April, I only made one small commit in March which is why it's not Feburary _to_ April.

If you've never heard of Prism before, it's my ultimate graphics study project that is the culmination of everything I've learned in graphics development so far. It is built upon years of hard effort/learning and also extremely valuable help from multiple people in the graphics community. You can find the complete source code and even more information on it's [Github repository](https://www.github.com/redstrate/prism).

### Vulkan is now moving to being a first-class backend

The Vulkan backend is moving very quickly to reach feature parity soon with the Metal version, but now it is
fully usuable for most tasks on Windows and Linux! The main roadblock right now is implementing the last of the
functionality required for IBL and some other graphical features.

![Screenshot of the material editor](/blog/img/PrismEditor_BT44VWksFY.png)
_This is the Material editor running on Vulkan, on Windows_

### SDL2 is the new default windowing system for Windows and Linux

Previously, I had hand-written Win32 code and XCB/XLib code for the Windows and Linux backends respectively. However, I had run into a few issues:

On Windows, my code was buggy and error prone. When getting around to implementing stuff like gamepads, multi-window support, I knew I didn't want to support this backend any longer.

On the Linux side, there was an even bigger issue - [Wayland](https://wayland.freedesktop.org/)! Wayland is the new display and window server protocol on Linux, and I wanted to support it. However, I had no interest in supporting pretty much two divergent Linux backends - one for X11 and one for Wayland. I had enough trouble supporting ~4 windowing backends and just duplicating the work on Linux seems too much.

Thus this is where using SDL2 became the perfect solution - I could have the _same_ code for Windows and Linux and it can run on Win32, Wayland and X11. That's pretty much three birds with one [industry-standard stone](https://youtu.be/MeMPCSqQ-34), which is pretty good! 

Right now SDL is used for Windows and Linux, and I have no plans on supporting it on macOS at the moment (even though it theroetically could). That's just because the macOS backend is the most feature complete, and the SDL2 backend is notably missing automatic theme detection as shown in the Windows screenshot featured above.

### Windows now has multiviewports!

{{< youtube 1WGRgIb9WJI >}}

This is a pretty and clear nice benefit from using the SDL backend, because now it gets multiviewport support for free! If you've never seen this [dear imgui feature before](https://github.com/ocornut/imgui/wiki/Multi-Viewports), it's really cool to see it in action. It allows regular imgui windows to be dragged outside of the main window, and enables some really cool workflows and usecases you would normally see in other GUI toolkits like Qt and GTK.

### The new render target system

Before if you wanted to render to another window, static image, viewport you were required to create a whole new renderer instance. This was bad design for a multitude of reasons - duplicated work, resources and lack of proper cohesion or synchronization. This was because a single renderer instance only supported rendering to one target. Now everything is reworked and I can use just one renderer instance for the whole engine, even down to the tooling!

![Screenshot of two viewports open at the same time](/blog/img/PrismEditor_Okvgr9cuI3.png)
_This is two editor viewports running at the same time in two different windows, something not possible before under the old system._

The new render target system is also the backbone of the new cross platform dear imgui multi-viewport support (try saying that 5x fast!) The API is also extremely easy to use:

```
auto render_target = renderer->allocate_render_target({100, 100});
```

Simply pass an extent, and you are returned a handle to the render target that you use for subsequent
resizing, destruction, etc. When you want to render, simply pass it to the `render` function:

```
renderer->render(commandbuffer, scene, render_target, -1);
```

### Shader live editing

As part of my on-going shader editing effort, I have finally implemented a form of shader editing you can perform in-engine:

This allows you edit basic shaders, but at the moment only the sky shader is using this new system. More shaders will be supported in the future, including editing the shader templates used by my material system. Here's an example of registering a live reload shader:

```
pipelineInfo.shaders.vertex_src = register_shader("sky.vert");
...
associate_shader_reload("sky.vert", [this] {
    createSkyPipeline();
});
```

Not only that, but it's built on top of preexisting GFX and Shader Compiler APIs, meaning that as long as your backend supports both it will happen transparently! This is fully supported by the Vulkan and Metal backends.

### New class and variable naming style

I have finally decided on a new, standard naming style for everything in Prism. It is pretty much the same style that the C++ STL uses, and I thought it would be the best going forward:

```
auto imgui = std::make_unique<prism::imgui_backend>();
```

Now everything is `snake_case`, following the function naming I'm already using. Private member variables are now changed to remove any underscores. I also used this chance to _finally_ move every class that I own into the `prism` namespace to reduce naming conflicts, which happen more often than you think (believe it or not, a lot of operating systems have a `Rectangle` structure!) It is still an ongoing process, but a lot of the major classes are already refactored.

### What's Next?

In the short term I want to keep working on polishing the Vulkan stuff, so I can eventually start working on some cooler things like VR support. I also plan to keep working on the example app more, so it can serve as a better showcase.

Some longer-term goals include DirectX support, an Android version, and eventually some form of raytracing/global illumination. I also want some easily accessible online documentation, leaveraging the pre-exsiting doxy docs that are included in the source code already.

Very soon I plan on working on the CI stuff some more so releases can be automatically built and published which would really help testing this on other people's machines (and also stop me from breaking other platform builds!)

**Edit:** I removed some old Github issue links that are now dead. Sorry!
