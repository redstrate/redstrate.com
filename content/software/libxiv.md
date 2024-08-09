---
title: "libxiv"
date: 2022-01-05
draft: false
layout: "project"
projtags:
- FFXIV
- Reverse Engineering
- CPlusPlus
aliases:
- /projects/libxiv
license: GPLv3
source: "https://github.com/redstrate/libxiv"
summary: "Unmaintained FFXIV modding framework."
---

I originally wrote this in C++, but eventually rewrote it in Rust and that turned into
[Physis]({{< ref "physis" >}}).

## Goals
* Easily integratable into other FFXIV launchers so they can have update/install support without having to write it themselves.
* Can export Penumbra/Lumina format mods, I have no interest in exporting in TexTools's format.
* Can export/edit some formats such as models, and metadata/exl files.
* Can be used on Windows/Linux/macOS and doesn't pull in a huge runtime (C#) or run in Wine.

## Features
* Easily extract game files and view excel sheets by name. See [gamedata.h](include/gamedata.h) for usage.
* Install patches (right now it's limited to boot patches). See [patch.h](include/patch.h) for usage.
* Install FFXIV by emulating the official installer, bypassing Wine and InstallShield. You can see how to use this in [installextract.h](include/installextract.h).
* Parse some game data:
  * [EXD](include/exdparser.h)
  * [EXH](include/exhparser.h)
  * [EXL](include/exlparser.h)
  * [FIIN](include/fiinparser.h)
  * [INDEX/INDEX2](include/indexparser.h)
  * [MDL](include/mdlparser.h)
