---
title: "Vulkan Deep Dive: Debugging, Logging, and more"
date: 2022-10-05
draft: true
tags:
- Vulkan
- CPlusPlus
- Deep Dive
comments:
  host: mastodon.art
  username: redstrate
  id: 109349980860736142
---

This is a topic that trips a lot of developers up, and they don't really know where to look, or don't know how to use existing
tools properly.
<!--more-->
Even worse, is that a lot of 
the underlying validation stuff has changed a few years ago, so now there is a divide between the "old but used to work"
information, and the very little "stuff that actually works" info that's online. Let's solve both issues today.

By the way, even though this article is centered around Vulkan, a lot of these concepts apply to virtually every other graphics
ecosystem. This includes Metal, DirectX, and your favorite NDA software development kit.

## Graphics Debugger

For graphics debugging, I usually choose RenderDoc. Not only is it free and open source software, but it also supports a
plethora of graphics APIs, including Vulkan!

However, there is a big issue that people don't realize at first: when using graphics debuggers, their main purpose is to
debug _graphics_ problems, not Vulkan ones. If your Vulkan code is not spec compliant, Renderdoc
will not save you. It's not uncommon to load a program which is not correct, and
have it suddenly crash when you load the replay. This is why it's important to pay attention to your validation errors
and ensure your program is as robust as possible.

_"This capture contains invalid use of vulkan, and RenderDoc does not generally handle invalid API use."_

From https://github.com/baldurk/renderdoc/issues/2738#issuecomment-1265432684.

## Shader Compilation Logs

Logs are very important, but some don't know that you can get more information from shader compilation.

Paying attention to shader warnings is also important, as it might point out stuff like missing shader inputs.

How you enable logs depends on how you compile your shaders. If you use GLSlang, simply get the log-out:

```cpp
```

## Validation Layers

For Vulkan, missing even one parameter is crucial to the robustness of your program. Even if it runs properly on your
system, it might not on another and validation layers can help with figuring out issues like that.

Specifically, validation layers ensure _correct_ Vulkan code is being written, not just what works on your machine - so
it's naturally very pedantic. Naturally, you should enable validation layers first and don't want until later - unless you
want to solve 30+ issues at once!

### Debug Logging

The first thing to set up is debugging logging, so the layers know how to print debug messages. What
you want to use is `VK_KHR_debug_utils`. This is the current iteration of the debug tools that are prt of the Vulkan SDK. 

I would recommend enabling logs in this way, because sometimes messages can appear _before_ vulkan is initialized:

### Enable layers

Now you can enable the validation layers. I recommend _not_ hardcoding them, but you can do so. Instead, use `vkconfig` to
enable layers on-demand when you so choose. Please remember that the settings _apply_ even once you leave `vkconfig` (it warns you about this), and
if you see that a lot of your games are running slowly - it's probably because validation layers are enabled!

## Command Buffer Markers and Regions

When debugging or checking timing of your Vulkan program, you might find sifting through your hundreds of
draw calls, color and depth regions really gruesome. Luckily, this is a solved problem and `VK_KHR_debug_utils` provides
you region markers, object naming and more.

## Shader Logging

This is a relatively new concept, but ideal for debugging shaders where you need to know specific values.
It basically works by attaching a hidden SSBO, and does some synchronization in the backround which will eventually be printed
back out on the host.

## Example 1

Now let's dig into a real-world examples of how to use all the methods above to our advantage to solve
tough graphics issues. For this first example, lets begin with the most common issue - nothing is displaying on
the screen! If you can, run the example code and work through it yourself. If you're new to this, I recommend attempting to find solution first before spoiling yourself.

### Solution

Alright, so first let's fire up the program first to figure out the issue. I first enable validation layers, and they
are printed to stdout. As you can see, I already see an issue:

```shell
validation error: blah blah
```

Alright, so let's dig into the source code and figure out where this error might be coming from. Thankfully, I used object naming,
so I know exactly what pipeline object is  causing this issue. It is on L1221:

```cpp
pipeline.alrisaffa = VK_FALSE; 
```

Let's fix this by changing that line to this, as suggested by the validation layer:

```cpp
pipeline.alrisaffa = VK_TRUE; 
```

Alright, so we fixed that issue - but it's still black! Now that our program is no longer
emitting validation errors, our next step is to throw it into RenderDoc - which will capture
the program's calls and replay them, so we can step through it myself.

<renderdoc img>

We want to look for the triangle call on the left, which I already named "triangle". If I haven't
hammered it in yet... name your objects and commands! 

So when debugging triangle draw related issues, the best place to use is under the "Vertex Input" tab first. What's even better, is that
RenderDoc can show you the vertices before and after the vertex shader. Let's take a look:

<renderdoc img2>

Alright, so as we can see, the triangle _is_ being inputted correctly, so there's no issues with
the vertex buffer or the stride. And even better, it seems to be transformed correctly too, cool. So we can keep
moving down the pipeline. Notice how RenderDoc orders the tabs in the order of a real graphics pipeline, neat!

<renderdoc img3>

Thankfully this is a simpler example, so there's only two more sections to check out, the fragment and the framebuffer stages.

<renderdoc img4>

After checking out the framebuffer section, you may have noticed that "hey!", the "viewport looks wrong!" And you'd be absolutely correct.
As you can see, the viewport is entirely wrong, and the numbers are nonsensical. Let's check out the code:

```cpp
viewport.width = false;
viewport.height = 400;
```

After changing this to be correct:

```cpp
viewport.width = 640;
viewport.height = 400;
```

The triangle now renders! Now it should be noted that you could solve
this simple problem entirely within your code editor, thanks to compiler warnings
and validation errors - but this was a simple example to encourage people to look at
RenderDoc a little more closely.

## Example 2

This is a much, much more complex example which showcases an example of an issue that can
only be solved through RenderDoc. Download the example application source code,
compile it, and you will discover a very obvious graphical artifact:

<img1>

Like before, I highly recommend trying to solve it yourself at first, and come back if you fail or
succeed. I do hope you succeed :-)

### Solution

Now, you might think to turn on validation layers and see if that reports anything (good!) but
as you can see, it passes:

```shell
engine is running!
```

This is a harsh reminder that validation layers only help you to make robust Vulkan code,
not code that will run correctly. Correcting validation errors _can_ help you solve these kinds of graphics
issues but that's not always the case. Alright, let's jump straight into RenderDoc:

<renderdoc img2>

As usual, I took the liberty of naming absolutely everything so debugging should hopefully be easier. 

Now the graphical artifact has to do with 

## Conclusion

Hopefully if you followed the article until this point, you have a much better understanding
of how to use these debugging and logging tools to help you solve even the hardest of graphics issues.

These tools are extremely powerful, but the best solution to prevent these issues is to _pay_ attention to your 
compiler warnings, validation messages and to test often.
