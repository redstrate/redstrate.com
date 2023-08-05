---
title: "Vulkan Deep Dive: Bokeh Depth of Field"
date: 2022-10-05
draft: true
tags:
- Vulkan
- CPlusPlus
- Deep Dive
---

Before we get into the technique we'll implement later, let's take a look down memory lane with depth of field in games:
<!--more-->

## Theory

As far as I know, there is no proper whitepaper for this technique (please contact me if there is!) and this instead an
amalgamation of different techniques made by different people. They are all credited below, and referenced accordingly.

The technique is unique where it sounds extremely simple in theory, but it is increasingly
complex once you start to implement, as you are breaking common graphics conventions.

First we want to choose a proper bokeh shape, as always hexagons are a common choice:

<hexagonal image>

Now, we want to _flood_ the screen with these. Seriously, I'm not joking - but _flood_. If you
have any intermediate experience in graphics development, you're probably screaming at you screen at the moment.
"The overdraw!! There's going to be so much overdraw!!", "The alpha blending is going to kill your frames!".

To solve this issue, smarter people have figured out the way to avoid these issues is two-fold:

* Limit the size of the bokeh to a balance between reasonably looking, and performant.
* Split the bokeh fields into near and far fields.


## Implementation
