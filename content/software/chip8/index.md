---
title: "chip8"
date: 2020-01-25
draft: false
source: "https://git.sr.ht/~redstrate/chip8"
license: MIT
tags:
- C++
- Emulation
resources:
- src: img/output.png
  name: Screenshot
layout: "project"
aliases:
- /projects/chip8
summary: "Basic Chip-8 emulator."
---

This is my first ever (working) emulator, of the simple CHIP-8 system. I'm pretty proud of this, because apart from the sprite collision logic I was able to implement most of the opcodes just looking at a basic overview of the instruction set.

![Screenshot of breakout](output.webp)

Technically, this implements the SCHIP type of instructions but can still play many of the ROMs you can find online. I also added a cute debugger window and a memory viewer. The emulator also comes with a built-in deflicker for the display.

For funsies, I included a basic parser that can spit out valid CHIP-8 instructions for a C-style language!
