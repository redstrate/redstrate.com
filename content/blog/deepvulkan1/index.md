---
title: "Vulkan Deep Dive: PCSS"
date: 2022-10-05
draft: true
tags:
- Vulkan
- C++
- Deep Dive
---

Hello and welcome to the first of many "Vulkan Deep Dives" I plan on writing this year. What are these?
<!--more-->
Well to put it simply, there is _a lot_ of Vulkan content on the Internet now. Which is great, but what ends up
happening is that someone gets knee-deep in writing their tutorial and end up losing steam once they get past the
"really basic 90%". This is stuff like initialization (boring), device creation (snooze), render passes (eugh) and pipeline creation (woo?).
There is a **lot** of these kind of tutorials out there, and I don't want to add to that pile. What I want to do instead, is show
you the 10% of your Vulkan renderer, the one that implements these cool techniques! I will also cover how
these techniques work in detail. If you wish to suggest topics, you can contact me through e-mail or reply to the Knockout thread.

Today we'll be covering PCSS, or Percentage Close Soft Shadows.

## Theory

For most naive soft shadow mapping techniques, there is usually a PCF or other similar kernel
applied uniformly to the whole map. This works if the shadows are far away, and not supposed to be
extremely detailed, but as games are becoming more "realistic" and the camera zooms farther and farther in - this becomes an issue.

Not only does it not like realistic, it also just doesn't look pretty. Because the kernel is applied
uniformly, it looks great as the shadow gets farther away but brings in artifacts and accidental peter-panning
as it the object gets closer to the shadow.

This is where PCSS comes in, which was originally pioneered by NVIDIA (https://developer.download.nvidia.com/whitepapers/2008/PCSS_Integration.pdf).
I recommend reading the paper beforehand, as it's an incredibly simple technique and the paper is very short. There is three basic ideas:

* Using high-precision depth textures.
* Implement blocker searching to vary PCF filter size.
* Use manually adjusted light sizes.

The first and last points are extremely easy, use a 32-bit floating point depth map, and you must be able to 
pass another light parameter to your shader. Where it gets interesting is how PCSS actually determines how to make
shadows soft, or hard.

<example PCSS>
_Note:_ Example of PCSS in action, Prism.

Before we continue, it's important to refresh how shadows work in real life. In short, when you point light
at an object, it "blocks" light. This is the essence of shadow. However, why do shadows get softer the farther away you get from a light?
This is because shadows bounce, and so does light. This creates a very noticeable transition:
TODO MENTION PENUMBRA

<example light photo>

So back to PCSS, the algorithm is extremely simple. First, we want to figure out (from the light's point of view), what is
blocking the light and what is not. If you remember when you first implemented shadow mapping, how it works is simple:
you draw a depth map from the light's point of view, and then you reconstruct the depth map from the camera point of view.
If you discover something is "above" your object from the light's point of view - then it is obstructed and needs to be sheathed
in darkness!

<example shadow mapping>

## Implementation

Alright, that's enough - we care about soft shadowing. If you remember, the farther away from the object, the softer
the shadow should be. Actually, let's call that object the "blocker". PCSS is broken up into these steps:

* Find the blocker for that pixel/fragment. This is of course, impossible, so we get the average.
    * The search width is dependent on the light size, which is tied to how large your shadow map is.
* If there is something blocking, then we must figure out the proper shadow penumbra, based off of the (average) blocker depth,
  and then we calculate a proper filter radius.
* Pass this new filter radius to PCF, or your favorite kernel .

And the results are _amazing_, let's take a look at a comparison between hard shadows, PCF shadows, and then PCSS+PCF:

<comparison slider>

Just this small change to calculate the blocker average depth gives a ton of realism to the scene, even
when nothing else has changed. However, there is a couple of drawbacks:

* The PCSS whitepaper only covers sun-type, infinite distance lights. How does PCSS integrate into say, point and spotlights?
* What is the cost of running PCSS compared to PCF?
* What is the correct "light size"?

Unfortunately the PCSS paper only covers light sources that are assumed to be infinitely far away, which is fine
but this technique is useful for things like spotlights. Thankfully, I have the relevant code below:


There are a few changes related to removing the parallel plane estimation, and the changes you have to make
to the shadow mapping in general, but it's pretty simple. The same can be said about point lights, as shown:

However, a word of warning, this is _extremely_ expensive. Let's do some really naive math:

* Assume we do 4 blocker samples, and 4 PCF samples.
* If we run on a 640x480 screen, assume this fragment shader is running on an object that covers the screen entirely.
    * We will assume the object is covered entirely by another object, or multiple of them. PCSS will always be run and cannot early-out.
* Sun and Spot lamps
    * (640 * 480) * 4 + 4 = 1,228,804 estimated depth map samples
* Point lights
    * (640 * 480) * 6 (4 + 4) = 14,745,600 estimated depth map samples

PCSS is _not_ cheap, and should be used sparingly. If you only apply it to just the main sun lamp in your
scene, it would easily be real-time - but scaling it to every kind of light will easily slow everything down. As shown,
point lights increase your depth samples by 1200%! Of course, you might turn down the samples, but imagine having even one more
point light in your scene. This is a similar problem with PCF applied to point lights,
but it is exacerbated with PCSS since we are easily doubling the samples or more.

When it comes to light size, it is not physically based but instead another knob or artists.

## Conclusion

PCSS is an extremely easy way to increase realism for your shadows, but at a possibly heavy
cost. I highly recommend implementing it into your engine, but definitely watch how many samples
it's using. Using it for point lights and spotlights result in great
looking scenery but is still not really possible in real-time.