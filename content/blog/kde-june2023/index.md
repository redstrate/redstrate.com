---
title: "My work in KDE for June 2023"
date: 2023-06-30
draft: true
tags:
- Linux
- Open Source
- KDE
- Qt
toc: true
series:
- My Work in KDE
---

We're over halfway through year! This update is a bit smaller than usual, and more focused on applications than Plasma. This isn't for lack of time or trying, but I made a conceited effort to clear out my MR backlog - fixing more issues than piling on features. This uh... didn't really work out and I'll be trying the same goal next month. I'm also going to explain a little bit of the reasoning behind this month's changes, so maybe it could inspire or help someone.

# Tokodon

The Android build (and CI) for Tokodon was broken ever since I replaced the video player with libmpv, so I spent a good chunk of this month making sure it's working again. This was quite a doozy, but I feel much more confident about improving Craft blueprints in the future.

To anyone who is not familiar with Craft, it's a meta build system created by KDE which is also used for the GitLab CI. Craft and it's blueprints are written in Python. Blueprints describe how to build the application or library, and has easy utilities for working with existing build systems (AutoTools, CMake, Meson, etc). It may be a little daunting, but these blueprints are extremely easy to write and maintain. More importantly, Craft enables easy cross-compilation since it contains blueprints for the underlying libraries for KDE applications: OpenSSL, zlib, and so on.

The problem is that Tokodon is - to my knowledge - the first KDE application to use libmpv on Android so I needed to break a lot of new ground to make this happen.

## zlib

zlib is already included in the Android NDK, but for some reason they don't ship pkgconfig files for it (for anything, really). This is troublesome, not for libraries or applications that link to zlib directly but as it turns out, other pkgconfig files. Libraries like freetype declare dependencies for zlib, and in turn pkgconfig will complain that it can't "find zlib" although the library itself exists, but not the pkgconfig file for it. Very annoying, I have some ideas on how we could solve this but for now, we now build it again on Android.

## kirigami-addons

This is a really simple fix, QtMultimedia was missing as a dependency for this library. The new FullscreenMaximizeDelegate component uses QtMultimedia under the hood to display video, but it wasn't declared in the blueprint.

## libarchive

When using libarchive for Android, you might encounter this error when including any of it's header:

```
<put error here>
```

But a quick search revels that this bug has been known and fixed, but there wasn't a new enough version in it's blueprint. Now it's bumped to 3.6.2, which includes the fix.

## ffmpeg

Tokodon uses libmpv to display videos from Mastodon and other services, which are served over HTTPS. libmpv uses ffmpeg to fetch video data along with playback, but the blueprint for ffmpeg did not enable any TLS backend yet. Now it enables the OpenSSL backend, since we already build it.

## fribidi and mpv

Here's probably the weirdest and honestly harder-than-it-should-be error I had to fix.

Here's a rundown of the necessary changes:
* Enable zlib on Android. This is necessary because Android NDK doesn't ship a pkgconfig for their built-in zlib.
* Kirigami-addons needed the QtMultimedia dependency (because of the new FullscreenImageDelegate component).
* libarchive needs to be bumped to 3.6.2, because of an Android build bug fixed in more recent versions.
* Enable OpenSSL support in ffmpeg, so there is HTTPs playback support.
* Build fribidi and mpv statically.

# Gamepad KCM

# Misc

* Two sticker fixes stickers in NeoChat
