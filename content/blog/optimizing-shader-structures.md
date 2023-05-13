---
title: "Optimizing and sharing shader structures"
date: "2023-05-13"
summary: "I use a lot of data structures in my shaders, including usage in push
constants and SSBOs. However, the complexity is getting out of hand!"
tags:
- Vulkan
---

In my engine I have a bunch of big data structures used in push constants,
shader buffers, and more. Typically, they are written for a machine first
and a human second (due to alignment, padding, and packing) which is not
ideal in my opinion. This comes with numerous issues, because the optimization
is hand-written and it's easy to create bugs due to mistyping or forgetting
alignment rules.

Here is one such example (real code, unfortunately) for exposing different
knobs and options to one of my post-processing steps:

```glsl
layout(push_constant) uniform PushConstant {
    vec4 viewport;
    vec4 options;
    vec4 transform_ops;
    vec4 ao_options;
    vec4 ao_options2;
    vec4 proj_info;
    mat4 cameraProj;
    mat4 invProj;
};
```

Can you tell me, with full confidence, what each of these options do? _I_
probably couldn't, and is a safe haven for bugs because it's
extremely easy to mix up accessors (e.g. `ao_options.x` and `ao_options.y`).
First, I want to explain some of the reasons why this is necessary in the
first place.

## Alignment rules in Vulkan

I want to give a real example that I see plenty of newer graphics programmers
run into. Say you're beginning to explore [Phong shading](https://en.wikipedia.org/wiki/Phong_shading), and you want
to expose a position and a color property so you can change them while the
program is running.

In a 3D environment, there's three axes (x, y and z) so our first choice is
a **vec3**. Light color would also make sense as a **vec3**, because color
(when emitted) from a light can't really be "transparent". The GLSL code
would end up looking like this:

```glsl
#version 430

out vec4 finalColor;

layout(binding = 0) buffer block {
    vec3 position;
    vec3 color;
} light;

void main() {
    const vec3 dummy = vec3(1) - light.position;
    finalColor = vec4(vec3(1.0, 1.0, 1.0) * light.color, 1.0);
}

```

_(There's no actual formula or anything in here, we just want to make sure
the GLSL compiler doesn't optimize anything out.)_

When writing the structure on the C++ side, you would naturally write this:

```cpp
struct Light {
    glm::vec3 position;
    glm::vec3 color;
} light;

light.position = {1, 5, 0};
light.color = {3, 2, -1};
```

For this example I used the [debug printf](https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/main/docs/debug_printf.md) system part of the Vulkan SDK[^1]. This allows us to get an exact reading of the
buffer as it's seen from the shader. The output is as follows:

```bash
Position = (1.000000, 5.000000, 0.000000)
Color = (2.000000, -1.000000, 0.000000)
```

Surprised? You might ask why is the last bit of the vector getting chopped
off - and someone might suggest writing the C++ structure like this instead:

```cpp
struct Light {
    glm::vec4 position;
    glm::vec4 color;
};
```

This seems to fix the issue:

```bash
Position = (1.000000, 5.000000, 0.000000)
Color = (3.000000, 2.000000, -1.000000)
```

But why does it suddenly work when we change to it a **vec4**? Fortunately the [the Vulkan specification](https://registry.khronos.org/vulkan/specs/1.3-extensions/html/vkspec.html#interfaces-resources-layout) is available and tells us why:

> The base alignment of the type of an OpTypeStruct member is defined recursively as follows:
> * A scalar has a base alignment equal to its scalar alignment.
> * A two-component vector has a base alignment equal to twice its scalar alignment.
> * **A three- or four-component vector has a base alignment equal to four times its scalar alignment.**
> * ...


That _third bullet point_ hits it right on the head, **vec4 and vec3 have the
_same_ alignment**, which you can also achieve by writing this:

```cpp
struct Light {
    glm::vec3 color;
    alignas(16) glm::vec3 position;
};
```

There's a bunch of more nitty and dirty alignment issues that stem from
differences between C++ and GLSL, this is just an example of one of them.
These are esoteric in my opinion, and it gets even harder to write decent
structures meant for humans - who are usually the ones writing shaders!

---

Another great example of odd cases of shader code not working when expected
is this shader block. Take a look at this four bool structure, which seems okay at
first glance:

```cpp
struct TestBuffer {
    bool a = false;
    bool b = true;
    bool c = false;
    bool d = true;
};
```

```glsl
layout(binding = 0) buffer readonly TestBuffer {
    bool a, b, c, d;
};
```

Oh wait... no, it's not actually okay:

```bash
a = 1, b = 0, c = 0, d = 0
```

I'm not exactly sure why it doesn't work and if anyone knows, please let me know.
It seems to be because [SPIR-V doesn't seem to define a physical
size for bool](https://registry.khronos.org/SPIR-V/specs/unified1/SPIRV.html#OpTypeBool),
so I'm not sure what it's represented as. Changing them to integers works
though.

Of course some might say this is a non-problem, because
_"Just use integers! they're just booleans!"_. I disagree, booleans and integers
are very different semantically for humans but of course less so for computers. You can also
pack a lot of booleans into the space of one 32-bit integer, which could be
a possible space-saving optimization.

## Sharing structures

One of the other problems I get annoyed with is keeping the structures
in sync, there's usually one (or many!) instances of the structure written in
C++ and many in GLSL. I even went through some of my shaders, and discovered
instances where I updated the structure in only some places and not others.
This is problematic because member order could change, meaning the structure
itself could be undefined (and can also easily escape notice, depending on
the shader is used).

Having just _one_ definition for all of my shaders and C++ would be a huge
improvement, even if I still had to pack and optimize manually.

## StructCompiler

What I ended up with is a new pre-processing step, called the **StructCompiler**.
I tried looking around on Google, and couldn't find anything similar - so I
don't know if this tool is actually unnecessary (maybe developers are instead
just pulling struct information from shader reflection?) but I did have a lot of
fun making it anyway.

It's goals are:
* Be able to define the shader structures in one, centralized file.
* Structures should be able to be written on a higher-level,
allowing us to decouple the actual member order, alignment and packing from
the logic.
* The structure can be reused in GLSL and C++.

First you write a `.struct` file. Here's the same, ugly post-processing
structure shown in the beginning, but now written in struct syntax[^2]:

```glsl
primary PostPushConstant {
    viewport: vec4
    camera_proj: mat4
    inv_proj: mat4
    inv_view: mat4

    enable_aa: bool
    enable_dof: bool

    exposure: float
    display_color_space: int
    tonemapping: int

    ao_radius: float
    ao_r2: float
    ao_rneginvr2: float
    ao_rdotvbias: float
    ao_intensity: float
    ao_bias: float
}
```

This one looks **much better**, doesn't it? Even without knowing anything
else about the actual shader, you can guess which options do what
with some accuracy. Here's what it looks like when compiled to C++:

```cpp
struct PostPushConstant {
    glm::mat4 camera_proj;
    glm::mat4 inv_proj;
    glm::mat4 inv_view;
    glm::vec4 viewport;
    glm::ivec4 enable_aa_enable_dof_display_color_space_tonemapping_;
    glm::vec4 exposure_ao_radius_ao_r2_ao_rneginvr2_;
    glm::vec4 ao_rdotvbias_ao_intensity_ao_bias_;
    ...
};
```

_(Setters like `set_exposure()` are used instead of accessing the glm::vec4 manually.)_

As I said before, the goal is to write it in a higher-level language which
can then be ruthlessly optimized without worry. The optimization is basic right
now, but it performs the same packing I did before by hand. Usage in GLSL is also easy:

```glsl
#use_struct(push_constant, post, post_push_constant)
```

_(The syntax could use some work, but the first argument is usage.
The second argument is the name of the struct, and the third argument is a unique name.)_

Since the member order and names are undefined, you must access the members by
a getter in GLSL. I think this is a worthwhile trade-off for more readable code, and
the compiler should optimize these away anyway.

```glsl
vec3 ao_result = pow(ao, ao_intensity())
```

This tool runs as a pre-processing step
in my offline shader system, but the struct files are copied into the runtime directory because
the runtime shaders also use them

The source code is [available here](https://git.sr.ht/~redstrate/structcompiler), which is just ripped from my engine tree. It's
quickly written, but it's already working and I have replaced all of my large structures already! I'm pretty happy with how this tool turned out, and I can't wait to explore how I can expand on this more.

[^1]: The debug printf, along with detailed examples of alignment mishaps is definitely future Graphics Dump material!

[^2]: The syntax looks eerily similar to Rust, which was intentional :-)
