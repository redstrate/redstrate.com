---
title: "Physis"
date: 2022-07-19
draft: false
layout: "project"
projtags:
- FFXIV
- Rust
- Reverse Engineering
aliases:
- /projects/physis
source: "https://github.com/redstrate/Physis"
license: GPLv3
summary: "Modding and data framework for FFXIV."
---

This is the successor to [libxiv]({{< ref "libxiv" >}}), which I originally wrote in C++. The language is not the only
difference however, as I learned a lot since originally writing libxiv which I have fixed in Physis. Compared to other
modding frameworks, this one is aiming to be all "batteries included" instead of exclusively focusing on texture modding,
data scraping, etc.

Physis features a C api which is accessed through the [libphysis](https://github.com/redstrate/libphysis) library. This
library should be usable through any language that can access the C FFI.

You can read more on it's [dedicated webpage on xiv.zone](https://xiv.zone/physis/). It's also published on [crates.io](https://crates.io/crates/physis)!
