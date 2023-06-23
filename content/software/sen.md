---
title: "Sen"
date: 2022-06-01
draft: false
layout: "project"
projtags:
- Kernel
- C
license: GPLv3
source: https://git.sr.ht/~redstrate/sen
summary: "Kernel for learning purposes."
---

This is my custom kernel for learning purposes. I'm not a osdev at all, so please excuse the mess.

Right now it compiles for x86_64, 32-bit is not supported. Most of this is just skeleton code from osdev.org, but I cleaned some stuff. I use Stivale for higher half kernel loading and not having to gaff about a bootloader for now. Limine is included as my bootloader of choice.
