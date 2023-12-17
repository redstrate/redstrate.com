---
title: "My work in KDE for December 2023"
date: 2023-12-30
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

# Tokodon

Fixed a bunch of papercuts with the Android build, and it should be publishing new versions to the F-Droid repository too! It's mostly adding missing icons and making sure it looks good in qqc2-breeze-style.

Fixed Akkoma and Pleroma tags not being detected correctly, so they should open in Tokodon instead of your web browser.

# Plasma

Fixed the tests on the CI to finally run, see [the KillTest fixes](https://invent.kde.org/plasma/kscreenlocker/-/merge_requests/191) and [pamTest fix](https://invent.kde.org/plasma/kscreenlocker/-/merge_requests/192). Failing tests now make the pipeline visibly fail, as it should.

# Kirigami

Fixed a bunch of TextArea bugs that affected mobile form factors, such as Plasma Mobile and Android. This is mostly for Tokodon (because we abuse TextAreas a lot in scrolling content) but it can help other applications too! The [selectByMouse property](https://invent.kde.org/plasma/qqc2-breeze-style/-/merge_requests/86) is now respected, [the cursor handles should show up less](https://invent.kde.org/plasma/qqc2-breeze-style/-/merge_requests/87),

Collapse [invisible MenuItems in qqc2-breeze-style like we do in qqc2-desktop-style](https://invent.kde.org/plasma/qqc2-breeze-style/-/merge_requests/88).

You can finally [right-click with a touchpad in qqc2-desktop-style TextFields again](https://invent.kde.org/frameworks/qqc2-desktop-style/-/merge_requests/337)! This bug has been driving me up a wall when testing our Qt6 stuff.

# Android

Added missing icons for [NeoChat](https://invent.kde.org/network/neochat/-/merge_requests/1465) and Tokodon. The next release should have less empty spots on screen!

Fixed [KWeather not launching on Android](https://invent.kde.org/utilities/kweather/-/merge_requests/97) due to missing QApplication! I also learned that QtCharts is Widgets-based.

I also went around and fixed up a bunch of other mobile applications with contributions too small to mention. Applications like Orca, Kongress, etc.

# Documentation

Fixed a [typo in PowerPlant's README](https://invent.kde.org/utilities/powerplant/-/merge_requests/18).

# Qt

My qmlformat patches described here are finally merging into Qt, and most of it will start appearing in 6.5, 6.6 and 6.7 releases.

# Outside of KDE

Nagged for a new QtKeychain release due to a critical bug that would cause applications to never open KWallet5. Please nag your distros to package 0.14.2 or else anything using the keychain won't work in Plasma 6! (This didn't affect people in the dev session, because qtkeychain is built from git.)

Also been helping the Gentoo KDE Team with packaging Plasma 6 and KDE Gear 6. I managed to update my desktop to Plasma 6 (yay!) and submitted fixes to get it closer to working. I also added [Arianna](), [PlasmaTube]() and [MpvQt]() packages.
