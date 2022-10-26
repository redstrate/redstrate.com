---
title: "Vulkan Deep Dive: Building your own editors"
date: 2022-10-05
draft: true
tags:
- Vulkan
- C++
- Deep Dive
---

Building editor and mod tools is something I never expected to find so enjoyable, and
it's another rabbit hole of endless programming goals.
<!--more-->
However, there is a distinct lack
of editor-focused graphics tutorials. Transform handles especially are troublesome, but we
will go over more than just that here.

## Wireframes and Debug Lines

## Billboards

## Transform Handles

When I first attempted to implement transform handles, I _struggled_. Since then, there has
been a few articles going over how to implement transform handles but none of them I really liked,
as I could copy and paste code from them all day, but I still don't understand the math behind it.

### Theory

Let's break down what's exactly going on when you use a transform handle. For this example, I would like to use Blenders:

<blender transform handke>

When you click and hold down the mouse button, the object _appears_ to move with it. You lock it to a specific axis, based
on which handle you grab - or do it all freeform. What's going on here? How is it able to associate movement on the screen with
movements in the scene?

The keyword is _view matrices_. Remember that for view matrices, it transforms from NDC to camera  space. However, think about how transform handles work - it's somehow associating
the screen position of the _object_ with the screen position of the _cursor_. So we need some way to reverse the view matrix, and
get the location of the object on the screen, or to put it more bluntly, in the _NDC_.

### Implementation

## Selecting Objects

Selecting objects on the screen is something else that is widely used, but another rare
talent alongside implementing transform handles. It's practically required for any kind of editing software,
much less those needed by 3D game engines. There are three main techniques for
handling this:

### Depth-based

### Color-based

### Occlusion Queries

## Graphical Interface

This is something not strictly graphics related, but I want to point out some common choices
for building the user interface outside the viewport.

### Qt

Qt is still a popular choice for building editor programs, for example - Source Filmmaker and the Source 2 SDK.

However, there is a huge upfront cost related to Qt, it requires a _lot_ of code to get running. Once you do the hard work though,
it's an extremely robust, supported and battle tested user interface. Performance is almost never an issue, and it supports
a lot of platforms out of the box. 

It should be noted that there is a common misconception that Qt forces your programs to be FOSS, which is
a non-option for many games. This is FUD, because as long as you link Qt libraries externally you are free to keep your
source code as closed as you want. And let me tell you, you will be using tens of megabytes worth of Qt libraries - there is very
little reason to link it statically. If you're really paranoid, you can pay the Qt
company an insubordinate amount of money for a proprietary licensed option... but why?

### Dear Imgui

Using Qt might not always be the best option for you, and "dear imgui" is becoming an increasingly popular option for many games, from indie to AAA games such as the upcoming GTA VI.

While "dear imgui" is suited to debug UIs for developers, it tends to fall apart when writing end-user UIs (which includes content creation tools)
however it is continuing to keep improving in this regard, especially with the docking branch.
With enough work, it can get pretty enough too, which you check out in the screenshot thread.

However, remember that it is meant for debugging UI's, so including images, icons, among other smaller
UI elements are more of an afterthought. For many developers though, that's an okay trade-off for how
easy it is to develop for.

### WPF or Win32

Win32 or WPF-based tooling is still popular for many developers, either due to the fact that most of your
content creators are using Windows, or because you run legacy software. See the Creation SDK, or Breath of the Wild:

<screenshot 1>
<screenshot 2>

However, there is some issues, for one using WPF in C++ is agony. It is easier if you write your tools in C#,
but then you're split between two languages (assuming you were using C/C++ in the first place). Win32 is a better
solution if you use C++, but it's extremely limited and Microsoft is no longer meaningfully maintaining it.