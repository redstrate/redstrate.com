---
title: "My work in KDE for December 2023"
date: 2023-12-30
draft: false
tags:
- Linux
- Open Source
- KDE
- Qt
toc: true
series:
- My Work in KDE
---

This is a lighter month due to holidays (and also I'm trying not to burn out), but I tried to fit in a bit of KDE anyway. It's all bugfixes anyway because of the feature freeze!

Not mentioned is a bunch of really boring busywork like unbreaking the stable branches of Gear applications due to the CI format changing.

# Tokodon

{{< add "bugfix" >}} Fixed a bunch of papercuts with the Android build, and the new nightlies should be appearing in [the F-Droid repository](https://community.kde.org/Android/F-Droid) soon! It's mostly [adding missing icons](https://invent.kde.org/network/tokodon/-/commit/59b14bff049eaa52f906274de2a2eb4792a3242b) and making sure [it looks good in qqc2-breeze-style](https://invent.kde.org/network/tokodon/-/commit/6149b58c4f3b407e6166a223542a2b6e744f0959) (the style we use on Android and Plasma Mobile.) {{< release "24.02" >}}

{{< add "bugfix" >}} Fixed [Akkoma and Pleroma tags not being detected correctly](https://invent.kde.org/network/tokodon/-/commit/8b98d9f0a7e897bcff0a5ff8d1b03d52f97b1a4e), they should open in Tokodon instead of your web browser again! {{< release "24.02" >}}

# Plasma

{{< add "bugfix" >}} KScreenLocker CI now runs supported tests, see [the KillTest fixes](https://invent.kde.org/plasma/kscreenlocker/-/merge_requests/191) and [pamTest fix](https://invent.kde.org/plasma/kscreenlocker/-/merge_requests/192). Failing tests also make the pipeline visibly fail, as it should. (Unfortunately, [the pipeline as of writing fails](https://invent.kde.org/plasma/kscreenlocker/-/jobs/1468399) to due some unrelated regression?) {{< release "6.0" >}}

{{< add "bugfix" >}} The lockscreen greeter [now handles even the fallback theme failing](https://invent.kde.org/plasma/kscreenlocker/-/merge_requests/193), and display the "please unlock using loginctl" message instead of a black screen. {{< release "6.0" >}}

{{< add "bugfix" >}} Improves the [QtQuickControls style selection mechanism](https://invent.kde.org/plasma/plasma-integration/-/merge_requests/126) to work around [a possible regression in Qt6](https://bugreports.qt.io/browse/QTBUG-120194). This should stop applications from mysteriously not opening in the rare (but unsupported) cases where our official styles aren't installed/loading. {{< release "6.0" >}}

# Kirigami

{{< add "bugfix" >}} Fixed a bunch of TextArea bugs that affected mobile form factors, such as Plasma Mobile and Android. This is mostly for Tokodon (because we abuse TextAreas a lot in scrolling content) but it can help other applications too! The [selectByMouse property](https://invent.kde.org/plasma/qqc2-breeze-style/-/merge_requests/86) is now respected, [the cursor handles should show up less](https://invent.kde.org/plasma/qqc2-breeze-style/-/merge_requests/87). {{< release "6.0" >}}

{{< add "bugfix" >}} [Invisible MenuItems in qqc2-breeze-style are collapsed like in qqc2-desktop-style](https://invent.kde.org/plasma/qqc2-breeze-style/-/merge_requests/88). Mobile applications should no longer have elongated menus with lots of blank space! {{< release "6.0" >}}

{{< add "bugfix" >}} You can finally [right-click with a touchpad in qqc2-desktop-style TextFields again](https://invent.kde.org/frameworks/qqc2-desktop-style/-/merge_requests/337)! This bug has been driving me up a wall when testing our Qt6 stuff. {{< release "6.0" >}}

{{< add "feature" >}} When the Kirigami theme plugin fails to load, [the error message will soon be a bit more descriptive](https://invent.kde.org/frameworks/kirigami/-/merge_requests/1411). This should make it easier for non-developers to figure out why Kirigami applications don't look correct. {{< release "6.0" >}}

# Android

{{< add "bugfix" >}} Fixed [KWeather not launching on Android](https://invent.kde.org/utilities/kweather/-/merge_requests/97) because it needed QApplication. I didn't know QtCharts is QWidgets-based! {{< release "24.02" >}}

I also went around and fixed up a bunch of other mobile applications with Android contributions too small to mention. Applications like [Qrca](https://invent.kde.org/utilities/qrca), [Kongress](https://invent.kde.org/utilities/kongress), etc.

# NeoChat

{{< add "bugfix" >}} Prevent the [NeoChat notification daemon from sticking around forever](https://invent.kde.org/network/neochat/-/merge_requests/1486) although that should rarely happen. {{< release "24.02" >}}

# Outside of KDE

[Nagged for a new QtKeychain release](https://github.com/frankosterfeld/qtkeychain/issues/244) due to a critical bug that would cause applications to never open KWallet5. Please also nag your distributions to package 0.14.2 soon! Anything using QtKeychain 0.14.1 or below won't work in Plasma 6. This doesn't affect people in the dev session, because QtKeychain should be built from git.

Helping the Gentoo KDE Team with packaging Plasma 6 and KDE Gear 6. I managed to update my desktop to Plasma 6 and submitted fixes to get it closer to working. I also added [Arianna](https://github.com/gentoo/kde/pull/954), [PlasmaTube](https://github.com/gentoo/kde/pull/952) and [MpvQt](https://github.com/gentoo/kde/pull/945) packages.
