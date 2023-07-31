---
title: "My work in KDE for July 2023"
date: 2023-07-29
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

The month of July is already wrapped up, I can't believe it! I went to Akademy 2023, if you want to read more details [about it here]({{< ref "akademy2023" >}}). I spent the majority of my time at airports or worrying about flights, so this month is a little bit shorter.

# Tokodon

The next release of Tokodon (23.08) is approaching next month, so I'm focusing on improving the application as quickly as I can. A round of [bugfixes for accounts](https://invent.kde.org/network/tokodon/-/merge_requests/283), [the fullscreen image viewer not closing](https://invent.kde.org/network/tokodon/-/merge_requests/284), [improving the conversation page](https://invent.kde.org/network/tokodon/-/merge_requests/285), [removing papercuts for statuses](https://invent.kde.org/network/tokodon/-/merge_requests/286), and [making the profile page even better](https://invent.kde.org/network/tokodon/-/merge_requests/287) landed early this month.

I now have a touchscreen Linux device so I've been able to [improve the touch experience for interaction buttons](https://invent.kde.org/network/tokodon/-/merge_requests/291). Expect more touch-related improvements in the future, before I only had a PinePhone and an Android device to test. Carl did a lot of profiling work, and I specifically [updated the blurhash implementation](https://invent.kde.org/network/tokodon/-/merge_requests/294) which makes it oh-so slightly faster to generate. I've been using git master to scroll my timeline recently, and it's super smooth now!

A big feature I've personally been waiting for has now landed, [an emoji picker for the status composer!](https://invent.kde.org/network/tokodon/-/merge_requests/304). I took this from NeoChat (of course) and slightly modified it for our needs. This is something that could use some improvement in the future, but I'm glad we have this now!

Another smaller but great feature is that [account mentions](https://invent.kde.org/network/tokodon/-/merge_requests/308) now open inside of Tokodon (like hashtags do already) without kicking you back to a web browser.

# PlasmaTube


