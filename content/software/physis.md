---
title: "Physis"
date: 2022-07-19T22:29:22-05:00
draft: false
tags:
- FFXIV
---

Collection of FFXIV modding and data-mining tools. Rust-based, and aiming for a stable C API.

<!--more-->
---

This is the successor to [libxiv]({{< ref "libxiv" >}}), which I originally wrote in C++. The language is not the only
difference however, as I learned a lot since originally writing libxiv which I have fixed in Physis. Compared to other
modding frameworks, this one is aiming to be all "batteries included" instead of exclusively focusing on texture modding,
data scraping, etc.

Physis features a C api which is accessed through the [libphysis](https://git.sr.ht/~redstrate/libphysis) library. This
library should be usable through any language that can access the C FFI.

You can read more on it's dedicated webpage on xiv.zone.