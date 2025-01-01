---
title: "Steam on Fedora Linux: \"Unable to retrieve clip information\""
date: "2025-01-01"
draft: false
tags:
- Steam
- Linux
---

I recently wanted to use the new Steam Game Recording feature, but I kept
running into a really annoying bug - I couldn't save anything! Trying to save it
to Steam's own media manager wouldn't do anything and not even give an error.
When trying to export it to a file, it would say "Unable to retrieve clip information (2)".

Fortunately, this is super simple to fix - it means Steam is unable to actually 
encode the video files. On Fedora Linux, going through
[RPMFusion's guide to installing codecs](https://rpmfusion.org/Howto/Multimedia)
managed to fix the Game Recording feature for me.
